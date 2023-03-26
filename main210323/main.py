import time
import discord
import requests
import re 
import logging
import random
import asyncio
import schedule
import datetime
from classManager import ProxyManager
from classManager import FirefoxDriver
from classManager import ChromeDriver
from classManager import RandomManager
from classManager import FileManager
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
proxyManager = ProxyManager()
fileManager = FileManager()
max_retry = 5
global activeDriver
#-----------global settings

#0 = chrome
#1 = firefox

r = random.randint(0,1)
if r == 0:
	print(f"{r} ChromeDriver")
	makeChrome = ChromeDriver.create()
	chromeOptions = ChromeDriver.chromeOptions()
	activeDriver = makeChrome.chromeDriver()
	try:
		while i != 5:
			proxy = proxy_manager.get_random_proxy()
			chromeOptions.add_argument("--proxy-server="+proxy)
			activeDriver.get("https://whatsmyip.com")
			if "Whats My" in activeDriver.title:
				break
			else:
				try:
					proxy_manager.remove_proxy(proxy)
				except Exception as e:
					print(e)
				activeDriver.quit()
				i +=1
		try:
			raw_ipv4 = WebDriverWait(activeDriver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/section/div/div/div/div[2]/p[1]')))
			ipv4 = raw_ipv4.text
			print(ipv4)
			activeDriver.quit()
		except Exception as e:
			print(e)	
	except Exception as e:
		print(e)
else:
	print(f"{r} FirefoxDriver")
	while i != maxretry:
		proxy = proxy_manager.get_random_proxy()
		activeDriver = FirefoxDriver(proxy=proxy).get_driver()
		activeDriver.get("https://whatsmyip.com")
		if "Whats My" in activeDriver.title:
			break
		else:
			try:
				proxy_manager.remove_proxy(proxy)
			except Exception as e:
				print(e)
			activeDriver.quit()
			i +=1
	try:
		raw_ipv4 = WebDriverWait(activeDriver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/section/div/div/div/div[2]/p[1]')))
		ipv4 = raw_ipv4.text
		print(ipv4)
		activeDriver.quit()
	except Exception as e:
		print(e)			
