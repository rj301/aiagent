"""
Tests for get_files_info.py
"""

from functions.get_files_info import get_files_info


def main():
    # Test current directory
    print("Result for current directory:")
    print(get_files_info("calculator", "."))
    print()

    # Test child directory
    print("Result for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))
    print()

    # Test directory outside permitted working area
    print("Result for '/bin' directory:")
    print(get_files_info("calculator", "/bin"))
    print()

    # Test directory outside permitted working area
    print("Result for '../' directory:")
    print(get_files_info("calculator", "../"))
    print()


if __name__ == "__main__":
    main()