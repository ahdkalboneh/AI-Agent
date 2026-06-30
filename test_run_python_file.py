from functions.run_python_file import run_python_file

# 1
print(run_python_file("calculator", "main.py"))

# 2
print(run_python_file("calculator", "main.py", ["3 + 5"]))

# 3
print(run_python_file("calculator", "tests.py"))

# 4
print(run_python_file("calculator", "../main.py"))

# 5
print(run_python_file("calculator", "nonexistent.py"))

# 6
print(run_python_file("calculator", "lorem.txt"))
