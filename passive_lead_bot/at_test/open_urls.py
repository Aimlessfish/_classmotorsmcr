import time
import discord
import requests
import re 
import logging
import random
import asyncio
import schedule
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import InvalidArgumentException

#-----------discord settings
intents = discord.Intents.default()
client = discord.Client(intents=intents)
#-----------discord settings

#-----------global settings
info_statement = "[INFO    ]"
logging.basicConfig(filename='lead_bot_errors.log', level=logging.ERROR)
#-----------global settings



def start():
	with open(r'C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\urls.txt', 'r') as file:
		url_pool = file.readlines()
	for url in url_pool:
		auto_trader_url = url
		retry_counter = 0
		max_retry = 3
		while retry_counter < max_retry:
			with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\proxy.txt") as f:
		 		proxies = f.readlines()
		 		global proxy
		 		proxy = random.choice(proxies).strip()
			with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\user-agents.txt") as f:
				user_agents = f.readlines()
				user_agent = random.choice(user_agents).strip()
			driver_options = webdriver.ChromeOptions()
			driver_options.add_argument("--proxy-server=http://"+proxy)
			driver_options.add_argument("--user-agent="+user_agent)
			driver_options.add_argument("--start-maximized")
			#-----------selenium settings
			driver_options.add_argument("--disable-blink-features=AutomationControlled")
			driver_options.add_experimental_option("excludeSwitches", ["enable-automation"])
			driver_options.add_experimental_option("useAutomationExtension", False)
			#-----------selenium settings
			driver = webdriver.Chrome(options = driver_options)
			# Changing the property of the navigator value for webdriver to undefined 
			driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
			try:
				driver.get(auto_trader_url)
				if "Auto Trader UK" in driver.title:
					print("Connected to AutoTrader..")
					break  # exit loop if page loaded successfully
			except Exception as e:
				logging.error(e, exc_info=True)
				retry_counter += 1
				now = datetime.datetime.now()
				timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
				print(f"{timestamp} {info_statement} [Console]: Proxy connection failed: retrying. {retry_counter}")
				if proxy in proxies:
					proxies.remove(proxy)  # remove proxy from list
					with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\working.txt", "w") as f:
						f.writelines(proxies)  # write updated list back to file
			try: #get price_text
				global listing_price
				find_price = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,"/html[1]/body[1]/div[2]/main[1]/div[1]/div[2]/aside[1]/section[1]/div[1]/div[1]/h2[1]")))
				if find_price:
					listing_price = find_price.text
			except InvalidArgumentException as e: #end get price
				logging.error(e, exc_info=True)
			i = 0
			while i < 1:
				try: 
					WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div[4]/iframe")))
					WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/div[2]/div[3]/div[2]/button[2]"))).click();
					i = i+1
				except TimeoutException as e:
					i = i+1
					#await message.channel.send("Time-out finding cookies element.")
					logging.error(e, exc_info=True)
					break
			driver.execute_script("window.scrollTo(0, 800)")
			try:
				global finance_option
				finance_option = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/main/div/div[2]/aside/section[3]/div/div/section/div/div[2]/div/button")))
				finance__text = finance_option.text
				print(finance__text)
			except TimeoutException as e:
				logging.error(e,exc_info=True)
				driver.quit()

start()