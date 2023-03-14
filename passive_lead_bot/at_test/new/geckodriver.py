import time
import discord
import requests
import re 
import logging
import random
import asyncio
import schedule
import datetime
import os
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
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from classManager import *

#-----------discord settings
intents = discord.Intents.default()
client = discord.Client(intents=intents)
#-----------discord settings

#-----------global settings
gecko_path = os.path.join(os.environ['SystemRoot'], 'geckodriver.exe')
binary_path = os.path.normpath(os.path.join(os.environ['ProgramFiles'], 'Mozilla Firefox', 'firefox.exe'))
firefox_service = FirefoxService(executable_path = gecko_path)
binary_location = binary_path
driver_options = webdriver.FirefoxOptions()
info_statement = "[INFO    ]"
logging.basicConfig(filename='lead_bot_errors.log', level=logging.ERROR)
#-----------global settings

max_retry = 5

#-----init class as object
randomManager = RandomManager()
proxyManager = ProxyManager()
fileManager = FileManager()
#-------------------------
# proxy = proxyManager.get_random_proxy()
# driver_options.add_argument("--proxy-server=http://"+proxy)
# driver_options.add_argument("--user-agent="+proxyManager.get_random_UA())
# driver_options.add_argument("-purgecaches")
# driver_options.add_argument("-private-window")
# driver = webdriver.Firefox(options=driver_options, firefox_binary=binary_location, service=firefox_service)
# driver.get("https://google.com")
# driver.quit()

async def ffscrapeAT():
	randomManager = RandomManager()
	proxyManager = ProxyManager()
	filemanager = FileManager()
	driver_options = webdriver.ChromeOptions()
	i = 0
	while i < max_retry:
		proxy = proxyManager.get_random_proxy()
		driver_options.add_argument("--proxy-server=http://"+proxy)
		driver_options.add_argument("--user-agent="+proxyManager.get_random_UA())
		driver_options.add_argument("-purgecaches")
		driver_options.add_argument("-private-window")
		driver_options.add_argument("--disable-blink-features=AutomationControlled")
		driver_options.add_experimental_option("excludeSwitches", ["enable-automation"])
		driver_options.add_experimental_option("useAutomationExtension", False)
		driver = webdriver.Firefox(options=driver_options, firefox_binary=binary_location, service=firefox_service)
		driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
		try:
			driver.get('https://autotrader.co.uk')
			if "New and Used" in driver.title:
				break  # exit loop if page loaded successfully
		except Exception as e:
			logging.error(e, exc_info=True)
			i += 1
			now = datetime.datetime.now()
			timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
			print(f"{timestamp} {info_statement} [Console]: Proxy connection failed: retrying. {i}")
			proxymanager.remove_proxy(proxy)
			await asyncio.sleep(2)

	if i == max_retry:
		now = datetime.datetime.now()
		timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
		print(f"{timestamp} {info_statement} [console]: Maximum retries met while running scrapeAT")
	await asyncio.sleep(10)

	try:
		WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div[4]/iframe")))
		WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/div[2]/div[3]/div[2]/button[2]"))).click();
	except TimeoutException as e:
		logging.error(e, exc_info=True)
		#await message.channel.send("Failed to accept cookies.")
	#navigate to refine search options
	try:
		more = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CLASS_NAME,"atds-hero__more-options")))
		more.click();
		postcode = driver.find_element(by=By.ID, value="postcode")
		postcode.click();
		postcode.send_keys(randommanager.get_random_postcode())
	except TimeoutException as e:
		logging.error(e, exc_info=True)
	await asyncio.sleep(5)
	try:
		WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//label[@for='Hatchback']//span[@class='body-type-selector__label atds-type-prius']"))).click();
		WebDriverWait(driver,6).until(EC.element_to_be_clickable((By.XPATH,"//label[@for='Estate']//span[@class='body-type-selector__label atds-type-prius']"))).click();
		WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH,"//select[@id='minPrice']"))).click();
		driver.find_element(By.XPATH,"//select/option[@value='1500']").click();
		await asyncio.sleep(2)
		# WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH,"//select[@id='maxPrice']"))).click();
		# driver.find_element(By.XPATH,"//select[@id='maxPrice']/option[@value='7500']").click();
		await asyncio.sleep(2)
		WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH,"//select[@id='maxMileage']"))).click();
		driver.find_element(By.XPATH,"//select[@id='maxMileage']/option[@value='150000']").click();
		await asyncio.sleep(2)
		driver.execute_script("window.scrollTo(0, 900)");
		WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//select[@id='minYear']"))).click();
		driver.find_element(By.XPATH,"//select[@id='minYear']/option[@value='2007']").click();
		await asyncio.sleep(1)
		driver.execute_script("window.scrollTo(0, 2500)");
		WebDriverWait(driver,6).until(EC.element_to_be_clickable((By.XPATH,"//select[@id='showWriteOff']"))).click();
		driver.find_element(By.XPATH,"//select[@id='showWriteOff']/option[@value='false']").click();
		WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//button[@type='submit']//*[name()='svg']"))).click();
		await asyncio.sleep(1)
		#await message.channel.send("Searching for new listings...")
	except TimeoutException as e:
		logging.error(e, exc_info=True)
		#await message.channel.send("failed to refine search")
	pageCount=5
	i=0
	filemanager = FileManager()
	while i < pageCount:
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')

		existing_urls = fileManager.urls

		for article in soup.find_all('article', class_='product-card js-standout-listing'):
			a_tag = article.find('a', class_='js-click-handler listing-fpa-link tracking-standard-link')
			if a_tag:
				url = a_tag['href']
				if 'http://autotrader.co.uk' + url + '\n' not in existing_urls:
					filemanager.write_url('http://autotrader.co.uk' + url)

		try:
			next_page_button = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a[class='paginationMini--right__active'] i[class='icon']")))
			if next_page_button:
				next_page_button.click()
				i += 1
			await asyncio.sleep(2)
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			i += 1
			#await message.channel.send("Couldn't get next page of listings")
	driver.quit()

async def start(leads_channel):
	await ffscrapeAT()
	print("finished......")
	await asyncio.sleep(10)

@client.event
async def on_ready():
	now = datetime.datetime.now()
	timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
	print(f'[{timestamp}] {info_statement} Logged in as [{client.user}]')
	guilds = client.guilds
	print(f'[{timestamp}] {info_statement} Connected to {len(guilds)} guild(s):')
	for guild in guilds:
		print(f'[{timestamp}] {info_statement} - {guild.name} (ID: {guild.id})')
		for channel in guild.channels:
			if channel.name == 'leads':
				print(f'[{timestamp}] {info_statement} - Found leads-channel in {guild.name} (ID: {guild.id}), channel ID: {channel.id}')
				global leads_channel
				leads_channel = client.get_channel(channel.id)
	# asyncio.create_task(run_schedule())
	asyncio.create_task(start(leads_channel))

if __name__ == '__main__':
    clientID = 'MTA2ODgzODc4OTM3MzUwOTY3Mg.GFApDS.0zYDIu4XqbBVsLrhwyK3WB2wok0gAVjA-Su85w'
    client.run(clientID)