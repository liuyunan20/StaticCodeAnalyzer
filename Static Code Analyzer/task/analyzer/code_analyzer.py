import re
import sys
import os


def check_error(path, code, num, blank_line):
    if len(code) > 79:
        print(f"{path}: Line {num}: S001 Too long")
    if code.strip("\n") != "" and (len(code) - len(code.lstrip())) % 4 != 0:
        print(f"{path}: Line {num}: S002 Indentation is not a multiple of four")
    if ";" in code and not re.search(r'#.*;', code) and not re.search(r"['\"].*;.*['\"]", code):
        print(f"{path}: Line {num}: S003 Unnecessary semicolon")
    if "#" in code and not code.startswith("#") and not re.match(r'.+\s{2,}#.*', code):
        print(f"{path}: Line {num}: S004 At least two spaces required before inline comments")
    if re.search(r'#.*[Tt][Oo][Dd][Oo].*', code):
        print(f"{path}: Line {num}: S005 TODO found")
    if code.strip("\n") != "" and blank_line > 2:
        print(f"{path}: Line {num}: S006 More than two blank lines used before this line")
    if code.strip().startswith("class"):
        if re.match(r'class\s{2,}.*', code.strip()):
            print(f"{path}: Line {num}: S007 Too many spaces after 'class'")
        class_name = code.lstrip("class").rstrip(":").strip("\n").lstrip()
        if not re.match(r'[A-Z]', class_name):
            print(f"{path}: Line {num}: S008 Class name '{class_name}' should use CamelCase")
    if code.strip().startswith("def"):
        if re.match(r'def\s{2,}.*', code.strip()):
            print(f"{path}: Line {num}: S007 Too many spaces after 'def'")
        func_name = code.lstrip("def").rstrip(":").strip("\n").lstrip()
        if not re.match(r'[a-z_]', func_name):
            print(f"{path}: Line {num}: S009 Function name '{func_name}' should use snake_case")


def get_path():
    base_path = sys.argv[1]
    paths = []
    if not base_path.endswith(".py"):
        for entry in os.listdir(base_path):
            if entry.endswith(".py"):
                paths.append(os.path.join(base_path, entry))
    else:
        paths.append(base_path)
    return sorted(paths)


for file_path in get_path():
    with open(file_path, 'r') as code_file:
        line_num = 0
        blank_lines = 0
        for line in code_file:
            line_num += 1
            if line.strip("\n") == "":
                blank_lines += 1
            else:
                check_error(file_path, line, line_num, blank_lines)
                blank_lines = 0
