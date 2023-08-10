import os
import argparse
import shutil
from colorama import Fore, Style

def find_htaccess_files(start_path):
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file == ".htaccess":
                yield os.path.join(root, file)

def check_Redirect_or_RewriteRule(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if 'Redirect' in line or 'RewriteRule' in line:
                return True
    return False

def copy_file_to_directory(file_path, start_path, target_directory):
    os.makedirs(target_directory, exist_ok=True)
    relative_path = os.path.relpath(file_path, start_path)
    new_file_name = relative_path.replace(os.sep, '_')
    target_path = os.path.join(target_directory, new_file_name)
    shutil.copy2(file_path, target_path)

def main():
    parser = argparse.ArgumentParser(description='Search for .htaccess files from a specific path.')
    parser.add_argument('--directory', required=True, help='The starting path to search for .htaccess files')

    args = parser.parse_args()
    found_Redirect_or_RewriteRule = False
    target_directory = "/data/web/migraties/htaccess/"

    for file in find_htaccess_files(args.directory):
        uses_Redirect_or_RewriteRule = check_Redirect_or_RewriteRule(file)
        if uses_Redirect_or_RewriteRule:
            print(Fore.GREEN + f'Path: {file} | Uses Redirect or RewriteRule: {uses_Redirect_or_RewriteRule}')
            print(Style.RESET_ALL, end='')
            found_Redirect_or_RewriteRule = True
            copy_file_to_directory(file, args.directory, target_directory)

    if not found_Redirect_or_RewriteRule:
        print(Fore.RED + 'No RewriteRule or Redirects found.')
        print(Style.RESET_ALL, end='')

if __name__ == "__main__":
    main()
