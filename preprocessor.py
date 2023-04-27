import sys
import os

class ModuleInfo:
    __slots__ = "name", "func_call", "body_text"
    def __init__(self, name, func_call, body):
        self.name = name
        self.func_call = func_call
        self.body_text = body

def process_file(file_path, indent=" " * 4, module_name=None, module_list=None, import_cursor=0):
    """Preprocesses a python script by recursively transcluding imported files."""
    # if not top level, returns the script without import statements
    if not os.path.exists(file_path):
        #print(file_path)
        return
    if module_list == None:
        module_list = []
        is_top_level = True
    else:
        is_top_level = False
        if any(module_info.name == module_name for module_info in module_list):
            raise RuntimeError(f"Detected cyclic import of module {module_name}.")
    with open(file_path, "r", encoding="utf-8") as file:
        module_buffer = []
        while True:
            line = file.readline()
            if not line:
                break
            words = line.strip().split(" ")
            if not len(words):
              module_buffer.append(line)  
            elif words[0] == "import" or words[0] == "from":
                path_segments = words[1].split(".")
                imported_module_name = path_segments[-1].strip()
                prev_imported_module = next((module for module in module_list if module.name == imported_module_name), None)
                all_module_exports = f"__{imported_module_name}_exports"
                if prev_imported_module:
                    func_call = prev_imported_module.func_call
                else:
                    imported_body_text = process_file(os.path.join(*path_segments).strip() + ".py",
                        indent=indent, module_name=imported_module_name, module_list=module_list,
                        import_cursor=import_cursor + 1)
                    if not imported_body_text:
                        # module not found. assume it's built in and leave the import statement intact
                        module_buffer.append(line)
                        continue
                    func_call = f"__import_{imported_module_name}()"
                    imported_module_buffer = [
                        f"def {func_call}:",
                        f"{indent}if \"{all_module_exports}\" in globals():",
                        f"{indent * 2}return globals()[\"{all_module_exports}\"]",
                        "",
                        f"{indent}# Begin imported file."
                    ]
                    imported_module_buffer.extend([indent + line for line in imported_body_text.splitlines()])
                    imported_module_buffer.append(
                        f"\n{indent}# End imported file.\n"
                        f"{indent}return locals()\n\n\n"
                    )
                if words[0] == "import" and (len(words) < 3 or words[2] != "as"):
                    import_mode = "import"
                    after_import_word_idx = 2
                elif words[0] == "import":
                    import_mode = "import as"
                    after_import_word_idx = 4
                elif words[0] == "from" and (len(words) < 5 or words[4] != "as"):
                    import_mode = "from import"
                    after_import_word_idx = 4
                elif words[0] == "from":
                    import_mode = "from import as"
                    after_import_word_idx = 6
                else:
                    raise RuntimeError("Typo?")
                import_only_line = " ".join(line.strip().split(" ")[:after_import_word_idx])
                module_buffer.append(f"global {all_module_exports}\n")
                func_call_line = [all_module_exports, "=", func_call]
                func_call_line.extend(line.strip().split(" ")[after_import_word_idx:])
                module_buffer.append(" ".join(func_call_line) + "\n")
                module_buffer.append(f"# {import_only_line}\n")
                if import_mode == "import":
                    module_buffer.append(
                        f"{imported_module_name} = __ModuleAttrDict({all_module_exports})\n"
                    )
                elif import_mode == "import as":
                    module_buffer.append(
                        f"{words[3]} = __ModuleAttrDict({all_module_exports})\n"
                    )
                elif import_mode == "from import":
                    if words[3] == "*":
                        module_buffer.append(
                            f"for k, v in {all_module_exports}.items():\n"
                            f"{indent}exec(k + \" = v\")\n"
                        )
                    else:
                        module_buffer.append(
                            f"{words[3]} = {all_module_exports}[\"{words[3]}\"]\n"
                        )
                elif import_mode == "from import as":
                    module_buffer.append(
                        f"{words[5]} = {all_module_exports}[\"{words[3]}\"]\n"
                    )
                else:
                    raise RuntimeError("Typo?")
                module_buffer.append("\n")

                if not prev_imported_module:
                    module_list.insert(import_cursor, ModuleInfo(imported_module_name, func_call,
                        "\n".join(imported_module_buffer)))
            else:
                if words[0] == "def" and is_top_level:
                    module_buffer.append(line[:line.find("def")] + "@__enhanced_debug_info\n")
                module_buffer.append(line)
        if is_top_level:
            strings = [
                f"class __ModuleAttrDict:\n",
                f"{indent}def __init__(self, dictionary=None):\n",
                f"{indent * 2}self.__dict__ = dictionary or {{}}\n",
                f"{indent}def __getitem__(self, key):\n",
                f"{indent * 2}return self.__dict__[key]\n",
                f"{indent}def __setitem__(self, key, value):\n",
                f"{indent * 2}self.__dict__[key] = value\n",
                f"def __enhanced_debug_info(func):\n",
                f"{indent}import functools\n",
                f"{indent}@functools.wraps(func)\n",
                f"{indent}def wrapped(*args, **kwargs):\n",
                f"{indent * 2}try:\n",
                f"{indent * 3}return func(*args, **kwargs)\n",
                f"{indent * 2}except BaseException as e:\n",
                f"{indent * 3}print('Source traceback (most recent call last):')\n",
                f"{indent * 3}frame_lines = []\n",
                f"{indent * 3}frame = e.__traceback__.tb_frame.f_back\n",
                f"{indent * 3}while frame:\n",
                f"{indent * 4}if not frame.f_back:\n",
                f"{indent * 5}module_name = '<top>'\n",
                f"{indent * 5}line_no = f'<untranslated:{{frame.f_lineno}}>'\n",
                f"{indent * 4}else:\n",
                f"{indent * 5}module_name, translated_line_no = __translate_line_no(frame.f_lineno)\n",
                f"{indent * 5}module_name += '.py'\n",
                f"{indent * 4}frame_lines.append(f'  File \"{{module_name}}\", line {{line_no}}, in {{frame.f_code.co_name}}')\n",
                f"{indent * 4}frame = frame.f_back\n",
                f"{indent * 3}print('\\n'.join(reversed(frame_lines)))\n",
                f"{indent * 3}print(type(e).__name__ + (': ' if str(e) else '') + str(e))\n",
                f"{indent * 3}exit()\n",
                f"{indent}return wrapped\n",
                f"def __translate_line_no(line_no):\n",
            ]
            after_translate_func = [
                f"{indent}else:\n",
                f"{indent * 2}raise ValueError(f'Failed to translate line {{line_no}} to source.')\n"
            ]
            running_line_num = len(strings) + len(after_translate_func) + 2 * len(module_list) # two lines added per module
            module_line_entries = []
            for module in module_list:
                module_line_entries.append(
                    f"{indent}{'if' if module == module_list[-1] else 'elif'} line_no >= {running_line_num}:\n"
                    f"{indent * 2}return '{module.name}', line_no - {running_line_num + 5}\n"
                )
                running_line_num += len(module.body_text.splitlines())
            strings.extend(reversed(module_line_entries))
            strings.extend(after_translate_func)
            strings.extend(module.body_text for module in module_list)
            strings.append("# End imports.\n")
            strings.extend(module_buffer)
            return "".join(strings)
        else:
            #print(f"module {module_name} preview:{''.join(module_buffer)}")
            return "".join(module_buffer)

if __name__ == "__main__":
    print(process_file(sys.argv[1]))
