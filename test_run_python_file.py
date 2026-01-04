"""
Tests for run_python_file.py
"""

from functions.run_python_file import run_python_file


def main():
    print("Expecting calculator usage instructions")
    print("Result:")
    print(run_python_file("calculator", "main.py"))
    print()

    print("Expecting run calculator with weird rendered result")
    print("Result:")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    print("Expecting should run calculator tests successfully")
    print("Result:")
    print(run_python_file("calculator", "tests.py"))
    print()

    print("Expecting to return an error")
    print("Result:")
    print(run_python_file("calculator", "../main.py"))
    print()

    print("Expecting to return an error")
    print("Result:")
    print(run_python_file("calculator", "nonexistent.py"))
    print()

    print("Expecting to return an error")
    print("Result:")
    print(run_python_file("calculator", "lorem.txt"))
    print()


if __name__ == "__main__":
    main()
