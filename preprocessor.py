import sys
import os

def process_file(file_path, indent="    ", module_name=None, module_list=None, import_cursor=0):
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
        if any(import_info.module_name == module_name for import_info in module_list):
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
                imported_module_name = path_segments[-1]
                print(module_list)
                matched_modules = [module for module in module_list if module.name == imported_module_name]
                if len(matched_modules):
                    imported_module_buffer = matched_modules.buffer
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
                        f"{indent}if '__imported_{imported_module_name}' in globals():",
                        f"{indent * 2}return",
                        f"{indent}global __imported_{imported_module_name} = True"
                    ]
                    imported_module_buffer.extend([indent + line for line in imported_body_text.splitlines()])
                if words[0] == "import" and (len(words) < 2 or words[1] != "as"):
                    imported_module_buffer.append(f"{indent}global {imported_module_name} = locals()")
                elif words[0] == "import":
                    imported_module_buffer.append(f"{indent}global {words[3]} = locals()")
                else: # words[0] == "from"
                    if words[3] == "*":
                        imported_module_buffer.append(f"{indent}globals().update(locals())")
                    imported_module_buffer.append(f"{indent}global {words[3]} = locals().{words[3]}")
                if not len(matched_modules):
                    module_list.insert(import_cursor, {"name": imported_module_name,
                        "func_call": func_call, "buffer": imported_module_buffer})
                module_buffer.append(func_call)
            else:
                module_buffer.append(line)
        if is_top_level:
            strings = ["\n".join(module.buffer) for module in module_list]
            strings.extend(module_buffer)
            return "".join(strings)
        else:
            return "\n".join(module_buffer)

if __name__ == "__main__":
    print(process_file(sys.argv[1]))