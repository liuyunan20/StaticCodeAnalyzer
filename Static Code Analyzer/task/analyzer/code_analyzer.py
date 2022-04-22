import re
import sys
import os
import ast


def check_error(path, code, num, blank_line, tree_result):
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
        for class_name in tree_result["class_names"]:
            if class_name in code:
                print(f"{path}: Line {num}: S008 Class name '{class_name}' should use CamelCase")
    if code.strip().startswith("def"):
        if re.match(r'def\s{2,}.*', code.strip()):
            print(f"{path}: Line {num}: S007 Too many spaces after 'def'")
        for func_name in tree_result["func_names"]:
            if func_name in code:
                print(f"{path}: Line {num}: S009 Function name '{func_name}' should use snake_case")
        for func_arg in tree_result["func_args"]:
            if func_arg in code:
                print(f"{path}: Line {num}: S010 Argument name '{func_arg}' should be snake_case")
        for func_name in tree_result["defaults"]:
            if func_name in code:
                print(f"{path}: Line {num}: S012 Default argument value is mutable")
    for variable_name in tree_result["variable_names"]:
        if variable_name in code and "=" in code:
            print(f"{path}: Line {num}: S011 Variable '{variable_name}' in function should be snake_case")
    # error_result += check_ast(code, path, num)
    # error_result.sort()
    # print(*error_result, sep="\n")


def check_ast(tree):
    tree_result = {"func_names": [], "func_args": [], "class_names": [], "variable_names": [], "defaults": []}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            if not re.match(r'[A-Z]', class_name):
                tree_result["class_names"].append(class_name)
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            if not re.match(r'[a-z_]', func_name):
                tree_result["func_names"].append(func_name)
            for func_arg in [a.arg for a in node.args.args]:
                if not re.match(r'[a-z_]', func_arg):
                    tree_result["func_args"].append(func_arg)
            for dft_arg in node.args.defaults:
                if isinstance(dft_arg, ast.List) or isinstance(dft_arg, ast.Set) or isinstance(dft_arg, ast.Dict):
                    tree_result["defaults"].append(func_name)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            if not re.match(r'[a-z_]', node.id):
                tree_result["variable_names"].append(node.id)
    return tree_result


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
    script = open(file_path).read()
    code_tree = ast.parse(script)
    tree_error = check_ast(code_tree)
    with open(file_path, 'r') as code_file:
        line_num = 0
        blank_lines = 0
        for line in code_file:
            line_num += 1
            if line.strip("\n") == "":
                blank_lines += 1
            else:
                check_error(file_path, line, line_num, blank_lines, tree_error)
                blank_lines = 0
