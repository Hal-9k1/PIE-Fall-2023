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
        print(file_path)
        return
    if not module_list:
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
            words = line.split(" ")
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
                module_buffer.append(line)
        if is_top_level:
            strings = [
                f"class __ModuleAttrDict:\n"
                f"{indent}def __init__(self, dictionary=None):\n"
                f"{indent * 2}self.__dict__ = dictionary or {{}}\n"
                f"{indent}def __getitem__(self, key):\n"
                f"{indent * 2}return self.__dict__[key]\n"
                f"{indent}def __setitem__(self, key, value):\n"
                f"{indent * 2}self.__dict__[key] = value\n\n"
            ]
            strings.extend(module.body_text for module in module_list)
            strings.append("# End imports.\n")
            strings.extend(module_buffer)
            return "\n".join(strings)
        else:
            #print(f"module {module_name} preview:{''.join(module_buffer)}")
            return "".join(module_buffer)

if __name__ == "__main__":
    print(process_file(sys.argv[1]))