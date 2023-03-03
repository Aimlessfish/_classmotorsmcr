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
import os
import time

os.system("title ProxySchedule")


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
		now = datetime.datetime.now()
		timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
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
			now = datetime.datetime.now()
			timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
			print(f"[{timestamp}] {info_statement} [Console]: proxies checked.")

def get_newProxy():
	now = datetime.datetime.now()
	timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
	print(f"[{timestamp}] {info_statement} [Console]: Clearing `working.txt`")
	with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\working.txt","w") as f:
		f.truncate(0)
		f.close()
	driver = webdriver.Chrome()
	driver.get("http://list.didsoft.com/get?email=sales@classmotorsmcr.co.uk&pass=Soontoberich1&pid=http3000&showcountry=no&https=yes&excludedcountry=CN|RU")
	proxyList = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > pre:nth-child(1)")))
	proxies = proxyList.text
	with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\proxy.txt","a") as f:
		f.write("\n"+proxies)
	print(f"[{timestamp}] {info_statement} [Console]: new proxies added.")
	driver.quit()
	time.sleep(10)
	testProxy()

async def run_schedule():
	now = datetime.datetime.now()
	timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
	print(f"[{timestamp}] {info_statement} [Console]: Starting schedule!")

	# times = ["06:00", "06:02", "07:00", "07:02", "07:30", "07:32", "08:00", "08:02", "09:00", "09:02", "09:30", "09:32", "10:00", "10:02", "10:30", "10:32", "12:00", "12:02", "12:30", "12:32", "13:00", "13:02", "13:30", "13:32", "14:00", "14:02", "14:30", "14:32", "15:00", "15:02", "15:30", "15:32", "16:00", "16:02", "16:30", "16:32", "17:00", "17:02", "17:30", "17:32", "18:00", "18:02", "18:30", "18:32", "19:00", "19:02", "19:30", "19:32", "20:00", "20:02", "20:30", "20:32", "21:00", "21:02", "21:30", "21:32", "22:00", "22:02", "22:30", "22:32"]

	# for t in times:
	#     schedule.every().day.at(t).do(get_newProxy)
	#     schedule.every().day.at(f"{t[:2]}:02").do(testProxy)
	schedule.every(15).minutes.do(get_newProxy)

	# schedule.every().day.at("06:00").do(get_newProxy)

	# schedule.every().day.at("07:00").do(get_newProxy)

	# schedule.every().day.at("07:30").do(get_newProxy)

	# schedule.every().day.at("08:00").do(get_newProxy)
	# schedule.every().day.at("08:15").do(get_newProxy)

	# schedule.every().day.at("09:00").do(get_newProxy)
	# schedule.every().day.at("09:15").do(get_newProxy)
	# schedule.every().day.at("09:30").do(get_newProxy)
	# schedule.every().day.at("09:45").do(get_newProxy)

	# schedule.every().day.at("10:00").do(get_newProxy)
	# schedule.every().day.at("10:15").do(get_newProxy)
	# schedule.every().day.at("10:30").do(get_newProxy)
	# schedule.every().day.at("10:45").do(get_newProxy)

	# schedule.every().day.at("11:00").do(get_newProxy)
	# schedule.every().day.at("11:15").do(get_newProxy)
	# schedule.every().day.at("11:30").do(get_newProxy)
	# schedule.every().day.at("11:45").do(get_newProxy)

	# schedule.every().day.at("12:00").do(get_newProxy)
	# schedule.every().day.at("12:15").do(get_newProxy)
	# schedule.every().day.at("12:30").do(get_newProxy)
	# schedule.every().day.at("12:45").do(get_newProxy)

	# schedule.every().day.at("13:00").do(get_newProxy)
	# schedule.every().day.at("13:15").do(get_newProxy)
	# schedule.every().day.at("13:30").do(get_newProxy)
	# schedule.every().day.at("13:45").do(get_newProxy)

	# schedule.every().day.at("14:00").do(get_newProxy)
	# schedule.every().day.at("14:15").do(get_newProxy)
	# schedule.every().day.at("14:30").do(get_newProxy)
	# schedule.every().day.at("14:45").do(get_newProxy)

	# schedule.every().day.at("15:00").do(get_newProxy)
	# schedule.every().day.at("15:15").do(get_newProxy)
	# schedule.every().day.at("15:30").do(get_newProxy)
	# schedule.every().day.at("15:45").do(get_newProxy)

	# schedule.every().day.at("16:00").do(get_newProxy)
	# schedule.every().day.at("16:15").do(get_newProxy)
	# schedule.every().day.at("16:30").do(get_newProxy)
	# schedule.every().day.at("16:45").do(get_newProxy)

	# schedule.every().day.at("17:00").do(get_newProxy)
	# schedule.every().day.at("17:15").do(get_newProxy)
	# schedule.every().day.at("17:30").do(get_newProxy)
	# schedule.every().day.at("17:45").do(get_newProxy)

	# schedule.every().day.at("18:00").do(get_newProxy)
	# schedule.every().day.at("18:15").do(get_newProxy)
	# schedule.every().day.at("18:30").do(get_newProxy)
	# schedule.every().day.at("18:45").do(get_newProxy)

	# schedule.every().day.at("19:00").do(get_newProxy)
	# schedule.every().day.at("19:15").do(get_newProxy)
	# schedule.every().day.at("19:30").do(get_newProxy)
	# schedule.every().day.at("19:45").do(get_newProxy)

	# schedule.every().day.at("20:00").do(get_newProxy)
	# schedule.every().day.at("20:15").do(get_newProxy)
	# schedule.every().day.at("20:30").do(get_newProxy)
	# schedule.every().day.at("20:45").do(get_newProxy)

	# schedule.every().day.at("21:00").do(get_newProxy)
	# schedule.every().day.at("21:15").do(get_newProxy)
	# schedule.every().day.at("21:30").do(get_newProxy)
	# schedule.every().day.at("21:45").do(get_newProxy)
	# schedule.every().day.at("21:00").do(get_newProxy)

	# schedule.every().day.at("22:00").do(get_newProxy)
	# schedule.every().day.at("22:15").do(get_newProxy)
	# schedule.every().day.at("22:30").do(get_newProxy)
	# schedule.every().day.at("22:45").do(get_newProxy)

	# schedule.every().day.at("23:00").do(get_newProxy)
	# schedule.every().day.at("23:15").do(get_newProxy)
	# schedule.every().day.at("23:30").do(get_newProxy)
	# schedule.every().day.at("23:45").do(get_newProxy)
	while True:
	    schedule.run_pending()
	    await asyncio.sleep(60)

get_newProxy()
asyncio.run(run_schedule())







