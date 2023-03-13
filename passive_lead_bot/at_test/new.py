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

max_retry = 5

class RandomManager:
	def __init__(self):
		self.namesfile = r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\names.txt"
		self.postcodefile = r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\postcode.txt"
		self.addressfile = r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\addresses.txt"
		self.names = []
		self.postcodes = []
		self.addresses = []
		self.load_names()
		self.load_postcodes()
		self.load_addresses()

	def load_names(self):
		with open(self.namesfile, "r") as f:
			self.names = [line.strip() for line in f]
			f.close()

	def load_postcodes(self):
		with open(self.postcodefile, "r") as f:
			self.postcodes = [line.strip() for line in f]
			f.close()

	def load_addresses(self):
		with open(self.addressfile, "r") as f:
			self.addresses = [line.strip() for line in f]
			f.close()

	def get_random_name(self):
		if not self.names:
			self.load_names()
		return random.choice(self.names)

	def get_random_postcode(self):
		if not self.postcodes:
			self.load_postcodes()
		return random.choice(self.postcodes)

	def get_random_address(self):
		ranAdd = random.choice(self.addresses).strip('"\n')
		street_town, postcode = ranAdd.rsplit(',',1)
		town = street_town.rsplit(',',1)[-1].strip()
		street = street_town.rsplit(',',1)[0].strip()
		houseNo = street.split()[0].strip()
		return houseNo, street, town, postcode

	def create_hpi_name(self):
		if not self.names:
			self.load_names()
		hpi_name = random.choice(self.names).strip()
		return name[:len(name)//2]+" "+name[len(name)//2]

	def random_phone(self):
		phone_suffix = str(random.randint(0,999999999)).zfill(9)
		phone_number= "07"+phone_suffix
		return phone_number

	def createEmail(self):
		global ranEmail
		ranEmail = self.randomEmail_name()+self.random_postCode()+"@prc.cx"
		with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\email.txt","w") as f:
			f.write(ranEmail)
			f.close()
		return ranEmail


class ProxyManager:
	def __init__(self):
		self.proxyfile = r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\proxy.txt"
		self.uafile = r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\user-agents.txt"
		self.useragents = []
		self.proxies = []
		self.load_proxies()
		self.load_UA()

	def load_proxies(self):
		with open(self.proxyfile, "r") as f:
			self.proxies = [line.strip() for line in f]

	def load_UA(self):
		with open(self.uafile, "r") as f:
			self.useragents = [line.strip() for line in f]

	def get_random_UA(self):
		if not self.useragents:
			self.load_UA()
		return random.choice(self.useragents)

	def get_random_proxy(self):
		if not self.proxies:
			self.load_proxies()
		return random.choice(self.proxies)

	def remove_proxy(self, proxy):
	    if proxy in self.proxies:
	        self.proxies.remove(proxy)
	        with open(self.proxyfile, "w") as f:
	            f.writelines(self.proxies)
	    else:
	        print(f"{proxy} not found in proxy list.")

class FileManager():
	def __init__(self):
		self.urlfile = r'C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\urls.txt'
		self.validfile = r'C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\valid_url.txt'
		self.urls = []
		self.validurls = []
		self.loadurl()
		self.loadvalid()

	def loadurl(self):
		with open(self.urlfile, "r") as f:
			self.urls = [line.strip() for line in f]
		return self.urls

	def loadvalid(self):
		with open(self.validfile, "r") as f:
			self.validurls = [line.strip() for line in f]
		return self.validurls

	def write_url(self, url):
		with open(self.urlfile, "a") as f:
			f.write(url+"\n")

	def write_valid(self, valid_url):
		with open(self.validfile, "a") as f:
			f.write(valid_url+"\n")

async def scrapeAT():
	randommanager = RandomManager()
	proxymanager = ProxyManager()
	filemanager = FileManager()
	driver_options = webdriver.ChromeOptions()
	i = 0
	while i < max_retry:
		proxy = proxymanager.get_random_proxy()
		driver_options.add_argument("--proxy-server=http://"+proxy)
		driver_options.add_argument("--user-agent="+proxymanager.get_random_UA())
		driver_options.add_argument("--start-maximized")
		driver_options.add_argument("--disable-blink-features=AutomationControlled")
		driver_options.add_experimental_option("excludeSwitches", ["enable-automation"])
		driver_options.add_experimental_option("useAutomationExtension", False)
		driver = webdriver.Chrome(options = driver_options) #- initialize instance 
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
			proxymanage.remove_proxy(proxy)
			await asyncio.sleep(2)

	if i == max_retry:
		now = datetime.datetime.now()
		timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
		print(f"{timestamp} {info_statement} [console]: Maximum retries met while running scrapeAT")
	await asyncio.sleep(10)

	try:
		WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div[4]/iframe")))
		WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.message-component.message-button.no-children.focusable.sp_choice_type_11.last-focusable-el"))).click();
	except TimeoutException as e:
		logging.error(e, exc_info=True)
		#await message.channel.send("Failed to accept cookies.")
	#navigate to refine search options
	try:
		more = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CLASS_NAME,"atds-hero__more-options")))
		more.click();
		postcode = driver.find_element(by=By.ID, value="postcode")
		postcode.click();
		postcode.send_keys(randommanage.get_random_postcode())
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

		existing_urls = filemanager.urls

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

async def checkFinance():
	randommanager = RandomManager()
	proxymanager = ProxyManager()
	filemanager = FileManager()
	now = datetime.datetime.now()
	timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
	print(f"{timestamp} {info_statement} [Console]: Proxy connection failed: retrying.")
	randommanage = RandomManager()
	proxymanage = ProxyManager()
	driver_options = webdriver.ChromeOptions()
	proxy = proxymanager.get_random_proxy()
	i = 0
	url_pool = filemanager.urls
	for url in url_pool:
		while i != max_retry:
			driver_options.add_argument("--proxy-server=http://"+proxy)
			driver_options.add_argument("--user-agent="+proxymanager.get_random_UA())
			driver_options.add_argument("--start-maximized")
			driver = webdriver.Chrome(options = driver_options)
			# Changing the property of the navigator value for webdriver to undefined 
			driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
			try:
				driver.get(url)
				if "Auto Trader UK" in driver.title:
					print("Connected to AutoTrader..")
					break  # exit loop if page loaded successfully
			except Exception as e:
				logging.error(e, exc_info=True)
				i += 1
				now = datetime.datetime.now()
				timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
				print(f"{timestamp} {info_statement} [Console]: Proxy connection failed: retrying. {retry_counter}")
				proxymanage.remove_proxy()
				await asyncio.sleep(2)
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
				i += 1
			except TimeoutException as e:
				i += 1
				#await message.channel.send("Time-out finding cookies element.")
				logging.error(e, exc_info=True)
				break
		driver.execute_script("window.scrollTo(0, 800)")
		try:
			finance_option = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/main/div/div[2]/aside/section[3]/div/div/section/div/div[2]/div/button")))
			if finance_option:
				filemanager.write_valid(driver.current_url+"\n")

		except TimeoutException as e:
			logging.error(e,exc_info=True)
			driver.quit()

async def start(leads_channel):
	await scrapeAT()
	print("finished......")
	await asyncio.sleep(10)
	await checkFinance()

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