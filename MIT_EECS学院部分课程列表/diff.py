import difflib
import argparse


def compare_python_files(file1_path, file2_path, ignore_comments=False):
    try:
        with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
            lines1 = file1.readlines()
            lines2 = file2.readlines()
            if ignore_comments:
                lines1 = [line for line in lines1 if not line.strip().startswith('#')]
                lines2 = [line for line in lines2 if not line.strip().startswith('#')]
            diff = difflib.unified_diff(lines1, lines2, fromfile=file1_path, tofile=file2_path, lineterm='', n=0)
            for line in diff:
                print(line, end='')
    except FileNotFoundError:
        print("Error: One of the files was not found.")
    except IOError:
        print("Error: Unable to read one of the files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare two Python files and show differences.')
    parser.add_argument('file1', help='First Python file path')
    parser.add_argument('file2', help='Second Python file path')
    parser.add_argument('--ignore-comments', action='store_true', help='Ignore lines starting with #')
    args = parser.parse_args()

    compare_python_files(args.file1, args.file2, args.ignore_comments)