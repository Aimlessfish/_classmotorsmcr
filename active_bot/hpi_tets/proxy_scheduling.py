#proxy scheduling

import requests
import discord
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import schedule
import asyncio


info_statement = "[INFO    ]"

session = requests.Session() 

def testProxy():
	now = datetime.datetime.now()
	timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
	print(f"[{timestamp}] {info_statement} [Console]: Checking proxies.")
	with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\proxy.txt","r") as f:
		proxy_list = f.read().split('\n')
#await message.channel.send("Checking 10 proxies..")
	proxies = proxy_list[0:10]
	for proxy in proxies:
		print(f"[{timestamp}] {info_statement} [Console]: proxy checked.")
		try: 
			response = session.get("http://ident.me/", proxies={'http': f"http://{proxy}"}, timeout=30)
			if response.status_code == 200: 
				proxy_list.pop(proxy_list.index(proxy))
				with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\proxy.txt","w") as f:
					f.write("\n".join(proxy_list))
				with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\working.txt","a") as f:
					f.write(f"{proxy} \n")
			else:
				proxy_list.pop(proxy_list.index(proxy))
				with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\proxy.txt","w") as f:
					f.write("\n".join(proxy_list))
		except Exception as e: 
			proxy_list.pop(proxy_list.index(proxy))
			with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\proxy.txt","w") as f:
				f.write("\n".join(proxy_list))
			print(f"[{timestamp}] {info_statement} [Console]: proxies checked.")

def get_newProxy():
	now = datetime.datetime.now()
	timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
	print(f"[{timestamp}] {info_statement} [Console]: Clearing `working.txt`")
	with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\working.txt","a") as f:
		f.truncate(0)
		f.close()
	driver = webdriver.Chrome()
	driver.get("http://list.didsoft.com/get?email=sales@classmotorsmcr.co.uk&pass=Soontoberich1&pid=http3000&showcountry=no&https=yes&excludedcountry=CN|RU")
	proxyList = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > pre:nth-child(1)")))
	proxies = proxyList.text
	with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\proxy.txt","a") as f:
		f.write("\n"+proxies)
	print(f"[{timestamp}] {info_statement} [Console]: new proxies added.")

async def run_schedule():
	now = datetime.datetime.now()
	timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
	print(f"[{timestamp}] {info_statement} [Console]: Starting schedule!")

	schedule.every().day.at("06:00").do(get_newProxy)
	schedule.every().day.at("06:02").do(testProxy)
	#schedule.every().day.at("06:00").do(lambda: asyncio.create_task(startScrape()))

	schedule.every().day.at("07:00").do(get_newProxy)
	schedule.every().day.at("07:02").do(testProxy)

	schedule.every().day.at("07:30").do(get_newProxy)
	schedule.every().day.at("07:32").do(testProxy)

	schedule.every().day.at("08:00").do(get_newProxy)
	schedule.every().day.at("08:02").do(testProxy)

	schedule.every().day.at("09:00").do(get_newProxy)
	schedule.every().day.at("09:02").do(testProxy)

	schedule.every().day.at("09:30").do(get_newProxy)
	schedule.every().day.at("09:32").do(testProxy)

	schedule.every().day.at("10:00").do(get_newProxy)
	schedule.every().day.at("10:02").do(testProxy)

	schedule.every().day.at("10:30").do(get_newProxy)
	schedule.every().day.at("10:32").do(testProxy)

	schedule.every().day.at("12:00").do(get_newProxy)
	schedule.every().day.at("12:02").do(testProxy)

	schedule.every().day.at("12:30").do(get_newProxy)
	schedule.every().day.at("12:32").do(testProxy)

	schedule.every().day.at("13:00").do(get_newProxy)
	schedule.every().day.at("13:02").do(testProxy)

	schedule.every().day.at("13:30").do(get_newProxy)
	schedule.every().day.at("13:32").do(testProxy)

	schedule.every().day.at("14:00").do(get_newProxy)
	schedule.every().day.at("14:02").do(testProxy)

	schedule.every().day.at("14:30").do(get_newProxy)
	schedule.every().day.at("14:32").do(testProxy)

	schedule.every().day.at("15:00").do(get_newProxy)
	schedule.every().day.at("15:02").do(testProxy)

	schedule.every().day.at("15:30").do(get_newProxy)
	schedule.every().day.at("15:32").do(testProxy)

	schedule.every().day.at("16:00").do(get_newProxy)
	schedule.every().day.at("16:02").do(testProxy)

	schedule.every().day.at("16:30").do(get_newProxy)
	schedule.every().day.at("16:32").do(testProxy)

	schedule.every().day.at("17:00").do(get_newProxy)
	schedule.every().day.at("17:02").do(testProxy)

	schedule.every().day.at("17:30").do(get_newProxy)
	schedule.every().day.at("17:32").do(testProxy)

	schedule.every().day.at("18:00").do(get_newProxy)
	schedule.every().day.at("18:02").do(testProxy)

	schedule.every().day.at("18:30").do(get_newProxy)
	schedule.every().day.at("18:32").do(testProxy)

	schedule.every().day.at("19:00").do(get_newProxy)
	schedule.every().day.at("19:02").do(testProxy)

	schedule.every().day.at("19:30").do(get_newProxy)
	schedule.every().day.at("19:32").do(testProxy)

	schedule.every().day.at("20:00").do(get_newProxy)
	schedule.every().day.at("20:02").do(testProxy)

	schedule.every().day.at("20:30").do(get_newProxy)
	schedule.every().day.at("20:32").do(testProxy)

	schedule.every().day.at("21:00").do(get_newProxy)
	schedule.every().day.at("21:02").do(testProxy)

	schedule.every().day.at("21:30").do(get_newProxy)
	schedule.every().day.at("21:32").do(testProxy)

	schedule.every().day.at("22:00").do(get_newProxy)
	schedule.every().day.at("22:02").do(testProxy)

	schedule.every().day.at("22:30").do(get_newProxy)
	schedule.every().day.at("22:32").do(testProxy)




	while True:
	    schedule.run_pending()
	    await asyncio.sleep(1)

asyncio.run(run_schedule())
