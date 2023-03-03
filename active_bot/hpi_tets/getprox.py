import requests
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

info_statement = "[INFO    ]"

session = requests.Session() 

def testProxy():
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {info_statement} [Console]: Checking proxies.")
    with open(r"C:\Users\notWill\Desktop\bot\cars\_classmotorsmain\required_list\proxy.txt","r") as f:
        proxy_list = f.read().split('\n')
    #await message.channel.send("Checking 10 proxies..")
    proxies = proxy_list[0:10]
    for proxy in proxies:
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {info_statement} [Console]: proxy checked.")
        try: 
            response = session.get("http://ident.me/", proxies={'http': f"http://{proxy}"}, timeout=30)
            if response.status_code == 200: 
                proxy_list.pop(proxy_list.index(proxy))
                with open(r"C:\Users\notWill\Desktop\bot\cars\_classmotorsmain\required_list\proxy.txt","w") as f:
                    f.write("\n".join(proxy_list))
                with open(r"C:\Users\notWill\Desktop\bot\cars\_classmotorsmain\required_list\working.txt","a") as f:
                    f.write(f"{proxy} \n")
            else:
                proxy_list.pop(proxy_list.index(proxy))
                with open(r"C:\Users\notWill\Desktop\bot\cars\_classmotorsmain\required_list\proxy.txt","w") as f:
                    f.write("\n".join(proxy_list))
        except Exception as e: 
            proxy_list.pop(proxy_list.index(proxy))
            with open(r"C:\Users\notWill\Desktop\bot\cars\_classmotorsmain\required_list\proxy.txt","w") as f:
                f.write("\n".join(proxy_list))
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {info_statement} [Console]: proxies checked.")

def get_newProxy():
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {info_statement} [Console]: Clearing `working.txt`")
    with open(r"C:\Users\notWill\Desktop\bot\cars\_classmotorsmain\required_list\working.txt","a") as f:
        f.truncate(0)
        f.close()
    driver = webdriver.Chrome()
    driver.get("http://list.didsoft.com/get?email=sales@classmotorsmcr.co.uk&pass=Soontoberich1&pid=http3000&showcountry=no&https=yes&excludedcountry=CN|RU")
    proxyList = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > pre:nth-child(1)")))
    proxies = proxyList.text
    with open(r"C:\Users\notWill\Desktop\bot\cars\_classmotorsmain\required_list\proxy.txt","a") as f:
        f.write("\n"+proxies)
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {info_statement} [Console]: new proxies added.")

get_newProxy()
testProxy()