
# README for `htaccess-find.py`

## Description
`htaccess-find.py` is a Python script designed to assist in identifying `.htaccess` files within a specified directory that utilize the `Redirect` or `RewriteRule` commands. If such files are found, they are copied to a designated target directory with a modified name reflecting their original path structure.

## Requirements

- Python 3
- `colorama` library (for colorful terminal outputs)

## Usage

```bash
python htaccess-find.py --directory [PATH_TO_DIRECTORY]
```

Replace `[PATH_TO_DIRECTORY]` with the path to the directory you want to start the search from.

## Features

1. **Recursive Search:** The script searches through the specified directory and all its subdirectories for `.htaccess` files.
2. **Command Checks:** For each found `.htaccess` file, the script checks for the presence of `Redirect` or `RewriteRule` commands.
3. **File Copy:** If a `.htaccess` file contains the specified commands, it is copied to `/data/web/migraties/htaccess/`. The copied file's name is based on its original relative path, with directory separators replaced by underscores.
4. **Colorful Outputs:** The script uses the `colorama` library to produce colorful terminal outputs for better readability.

## Example Output

```
Path: /path/to/found/.htaccess | Uses Redirect or RewriteRule: True
```

### License
[MIT](https://github.com/hpowernl/Bash-scripts/blob/main/LICENSE)
