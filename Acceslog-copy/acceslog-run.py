import os
import shutil
import hashlib
import datetime

def get_file_checksum(filename):
    h = hashlib.sha1()
    
    with open(filename, 'rb') as file:
        chunk = file.read(8192)
        while chunk:
            h.update(chunk)
            chunk = file.read(8192)
    return h.hexdigest()

src_file = "/var/log/nginx/access.log.1" # Acceslog location
dst_dir = "/data/web/acceslogs" # Save location
checksum_file = os.path.join(dst_dir, "checksum.txt")

if not os.path.exists(src_file):
    print(f"File {src_file} does not exist.")
    exit(1)

new_checksum = get_file_checksum(src_file)

if os.path.exists(checksum_file):
    with open(checksum_file, 'r') as f:
        old_checksum = f.read().strip()
else:
    old_checksum = None

if old_checksum == new_checksum:
    print(f"File {src_file} has not been changed. Script exits.")
    exit(0)

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

today = datetime.date.today()
dst_file = os.path.join(dst_dir, f"{today}-access.log")
shutil.copy2(src_file, dst_file)

with open(checksum_file, 'w') as f:
    f.write(new_checksum)

print(f"Copy from {src_file} has been successfully saved as {dst_file} and checksum is updated.")
