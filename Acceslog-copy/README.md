# Access Log Copier
This Python script monitors a specific access log file and copies it to a specified directory when it changes.

## How It Works
- The script calculates the SHA1 checksum of the monitored file.
- If this checksum is different from the previously stored one, it indicates that the file has changed.
- The script then copies the changed file to a specified directory and updates the stored checksum.
- The copied file is named with the current date and the extension .log.

## File Locations
The default locations are as follows:

- Monitored file: "/var/log/nginx/access.log.1"
- Destination directory: "/data/web/acceslogs"
- Checksum storage: A file named "checksum.txt" in the destination directory

You can modify these locations directly in the script.

## Usage
Run the script in a Python environment. It does not require any command line arguments. 
You will need write permissions for the destination directory and read permissions for the monitored file and checksum file.

## Contribution
Feel free to submit pull requests for bug fixes or improvements.

## License
[MIT](https://choosealicense.com/licenses/mit/)
