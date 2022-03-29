file_path = input()
with open(file_path, 'r') as code_file:
    line_num = 0
    for line in code_file:
        line_num += 1
        if len(line) > 79:
            print(f"Line {line_num}: S001 Too long")
