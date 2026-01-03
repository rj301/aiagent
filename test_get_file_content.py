"""
Tests for get_file_content.py
"""

from functions.get_file_content import get_file_content


def main():
    # Test current directory
    print("Result for main in current directory:")
    print(get_file_content("calculator", "main.py"))
    # print("------------------------------------------------------------------------------")
    print()

    # Test child directory
    print("Result for pkg/calculator.py in calculator directory:")
    print(get_file_content("calculator", "pkg/calculator.py"))
    # print("------------------------------------------------------------------------------")
    print()

    # Test directory outside permitted working area
    print("Result for '/bin/cat' file in calculator directory:")
    print(get_file_content("calculator", "/bin/cat"))
    # print("------------------------------------------------------------------------------")
    print()

    # Test non-existent file
    print("Result for 'pkg/does_not_exits.py' in calculator directory:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    # print("------------------------------------------------------------------------------")
    print()


if __name__ == "__main__":
    main()