#coded by AimlessFish
#29/01/23 - added function which scrapes each results page and parses the HTML for <a class="js-click-handler listing-fpa-link tracking-standard-link"
#appends all URLs to urls.txt with 'http://autotrader.co.uk' as prefix.
#should close out of the loop and quit the driver when last page is reached - not tested there's like 32,000 pages or something daft like that

#10/02/23 - in the 11 day gap:
# - removed cv2 & pytesseract usage
# - replace with get_plate function
# - added all random() functions
# - added logging
# - retrieve listing price
# - added all rquired .txt for random() functions
# - added feature to get HPIValuations > enter reg > signup
# - added feature to retrieve mailbox > retrieve valuation_url
# - added scrape hpi_trade_low/hi
# - added compare_() 
import time
import discord
import requests
import re 
import logging
import random
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
import asyncio
import datetime

logging.basicConfig(filename='errors.log', level=logging.ERROR)
driver_options = webdriver.ChromeOptions()

info_statement = "[INFO    ]"
now = datetime.datetime.now()
timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

##########
# discord
# settings
##########
intents = discord.Intents.default()
client = discord.Client(intents=intents)
reg_channel = client.get_channel(1076889006203207772)
#driver_options.add_argument("--headless")
#driver_options.add_argument("--disable-gpu")

##########
# global
# variables
##########
span_trade_high = ''
foreCourt_span_low = ''
foreCourt_span_high = ''
private_span_low = ''
private_span_high =  ''
val_link = ''
span_trade_low = ''
span_trade_high = ''

def ranFName():
	with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\names.txt","r") as f:
		first = f.readlines()
	return random.choice(first).strip()

def ranLName():
	with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\names.txt","r") as f:
		last = f.readlines()
	return random.choice(last).strip()

def randomEmail_name():
    with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\names.txt", "r") as f:
        names = f.readlines()
    return random.choice(names).strip()


def random_postCode():
	with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\postcode.txt","r") as f:
		postcode = f.readlines()
	return random.choice(postcode).strip()


def hpi_name():
	with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\names.txt","r") as f:
		names = f.readlines()
	name = random.choice(names).strip()
	return name[:len(name)//2]+" "+name[len(name)//2]

def random_phone():
	phone_suffix = str(random.randint(0,999999999)).zfill(9)
	phone_number= "07"+phone_suffix
	return phone_number

def random_address():
    with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\addresses.txt","r") as f:
        addresses = f.readlines()
        ranAdd = random.choice(addresses).strip('"\n')
    street_town, postcode = ranAdd.rsplit(',',1)
    town = street_town.rsplit(',',1)[-1].strip()
    street = street_town.rsplit(',',1)[0].strip()
    houseNo = street.split()[0].strip()
    return houseNo, street, town, postcode

ranEmail = randomEmail_name()+"."+random_phone()+"@yopmail.com"
with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\email.txt","w") as f:
	f.write(ranEmail)
	f.close()

##########################
# define !reg {args}
# input numplate 
# return valuation price
##########################
# proxy_usage_counter = 0
async def reg(message, *args):
	registration = str(*args)
	retry_counter = 0
	max_retry = 3
	while retry_counter < max_retry:
		with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\proxy.txt") as f:
	 		proxies = f.readlines()
	 		proxy = random.choice(proxies).strip()
		with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\user-agents.txt") as f:
			user_agents = f.readlines()
			user_agent = random.choice(user_agents).strip()
		driver_options.add_argument("--proxy-server=http://"+proxy)
		driver_options.add_argument("--user-agent="+user_agent)
		#await message.channel.send("Current proxy: "+proxy)
		#await message.channel.send("Current user_agent: "+user_agent)
		driver_options.add_argument("--start-maximized")
		driver = webdriver.Chrome(options = driver_options)
		try:
			driver.get('https://hpivaluations.com')
			if "Free" in driver.title:
				break  # exit loop if page loaded successfully
		except Exception as e:
			print(f"{timestamp} {info_statement} [Console]: Proxy connection failed: retrying. {retry_counter}")
			logging.error(e, exc_info=True)
			retry_counter = retry_counter+1
			await asyncio.sleep(2)
		#wait for page to load
		await asyncio.sleep(2)
	if retry_counter == max_retry:
		print(f"{timestamp} {info_statement} [console]: Maximum retries met while running !reg")
	else:
		try:
			# driver.find_element((By.ID,'onetrust-button-group-parent'))
			# driver.find_element((By.CLASS_NAME,'ot-sdk-three ot-sdk-columns has-reject-all-button'))
			cookies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#onetrust-accept-btn-handler")))
			cookies.click()
		except Exception as e:
			#await message.channel.send("Failed to accept cookes") 
			logging.error(e, exc_info=True)
		#enter reg
		await asyncio.sleep(2)
		try:
			enter_reg = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH,"//input[@placeholder='Enter Reg...']")))
			enter_reg.click();
			enter_reg.send_keys(*args)
			asyncio.sleep(2)
			if not cookies:
				WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.icon.icon-navigateright'))).click();
			else:
				cookies.click();
		except Exception as e:
			#await message.channel.send("Failed to search. Error finding search button.")
			logging.error(e, exc_info=True)
		await asyncio.sleep(2)
		try:
			WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH,'//span[normalize-space()="I don\'t own this car"]'))).click();
			await asyncio.sleep(2)
			WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='hpiconsentCheckbox']"))).click();
			WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='consentCheckbox']"))).click();
			await asyncio.sleep(2)
			WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='btn btn-primary radius js-modal-terms-cta']"))).click();
			await asyncio.sleep(2)
		except Exception as e:
			#await message.channel.send("Failed to declare ownership & accept terms")
			logging.error(e, exc_info=True)
		try:
			name = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='formName']")))
			name.click();
			name.send_keys(hpi_name())
		except Exception as e:
			#await message.channel.send("Failed to enter name")
			logging.error(e, exc_info=True)
		try:
			email = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='formEmail']")))
			email.click();
			email.send_keys(ranEmail)
		except Exception as e:
			#await message.channel.send("Failed to enter email")
			logging.error(e, exc_info=True)
		try:
			postal = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='formPostcode']")))
			postal.click();
			postal.send_keys(random_postCode())
		except Exception as e:
			#await message.channel.send("Failed to enter postcode")
			logging.error(e, exc_info=True)
		try:
			phone = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='formTelephone']")))
			phone.click();
			phone.send_keys(random_phone())
		except Exception as e:
			#await message.channel.send("Failed to enter phone number")
			logging.error(e, exc_info=True)
		try:
			WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='btn btn-primary onboarding__btn onboarding__btn--next']"))).click();
			await asyncio.sleep(2)
			try:
				global span_trade_low
				span_trade_low = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CLASS_NAME,"valuation__value__price__content")))
			except TimeoutException as e:
				logging.error(e,exc_info=True)
			if not span_trade_low:
				try:
					driver.get('https://yopmail.com')
				except TimeoutException as e:
					logging.error(e, exc_info=True)							
				try:
					WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#accept"))).click();
				except TimeoutException as e:
					logging.error (e, exc_info=True)
				try:
					login=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#login")))
					login.click()
					login.send_keys(ranEmail)
					time.sleep(1)
					WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".material-icons-outlined.f36"))).click();
					iframe = driver.find_element(By.ID,"ifmail")
					driver.switch_to.frame(iframe)
					valuation = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//a[normalize-space()='View valuation']")))
					val_link = valuation.get_attribute("href")

				except Exception as e:
					#await message.channel.send("Failed to retrieve mailbox.")
					logging.error(e, exc_info=True)
				#get hpi_price 
				try:
					driver.get(val_link)
					try:
						WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#onetrust-accept-btn-handler"))).click();
					except Exception as e:
						logging.error(e,exc_info=True)
					try:
						hpi_trade_low = span_trade_low.text.split()[0]
						global span_trade_high
						span_trade_high = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div/span[3]/span[1]")))
						hpi_trade_high = span_trade_high.text.split()[0]
					except TimeoutException as e:
						logging.error(e,exc_info=True)
					try:
						WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[2]"))).click();
						try:
							global foreCourt_span_low
							foreCourt_span_low = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/span[1]/span[1]")))
							foreCourt_low = foreCourt_span_low.text.split()[0]
							try:
								global foreCourt_span_high
								foreCourt_span_high = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/span[3]/span[1]")))
								foreCourt_high = foreCourt_span_high.text.split()[0]
							except TimeoutException as e:
								logging.error(e,exc_info=True)
						except TimeoutException as e:
							logging.error(e, exc_info=True)
					except TimeoutException as e:
						logging.error(e,exc_info=True)
					try:
						WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[1]"))).click();
						try:
							global private_span_low
							private_span_low = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/span[1]/span[1]")))
							private_sale_low = private_span_low.text.split()[0]
							try:
								global private_span_high
								private_span_high = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/span[3]/span[1]")))
								private_sale_high = private_span_hgih.text.split()[0]
							except TimeoutException as e:
								logging.error(e,exc_info=True)
						except TimeoutException as e:
							logging.error(e,exc_info=True)
					except TimeoutException as e:
						logging.error(e,exc_info=True)
					intents = discord.Intents.default()
					client = discord.Client(intents=intents)
					await message.channel.send("Evalutation for reg: " + registration)
					await message.channel.send("Trade low: " + hpi_trade_low)
					await message.channel.send("Trade high: " + hpi_trade_high)
					await message.channel.send("foreCourt_low: " + foreCourt_low)
					await message.channel.send("foreCourt_high" + foreCourt_high)
					await message.channel.send("private_sale_low" + private_sale_low)
					await message.channel.send("private_sale_high" + private_sale_high)
					driver.quit()
				except Exception as e:
					#await message.channel.send("Failed to get evaluation link")
					logging.error(e, exc_info=True)
			else:
				driver.wait_until_ready()
				try:
					
					span_trade_high = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div/span[3]/span[1]")))
					hpi_trade_high = span_trade_high.text.split()[0]				
				except TimeoutException as e:
					logging.error(e,exc_info=True)
				try:
					WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[2]"))).click();
					try:						
						foreCourt_span_low = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/span[1]/span[1]")))
						foreCourt_low = foreCourt_span_low.text.split()[0]
						try:							
							foreCourt_span_high = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/span[3]/span[1]")))
							foreCourt_high = foreCourt_span_high.text.split()[0]
						except TimeoutException as e:
							logging.error(e,exc_info=True)
					except TimeoutException as e:
						logging.error(e, exc_info=True)
				except TimeoutException as e:
					logging.error(e,exc_info=True)
				try:
					WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[1]"))).click();
					try:						
						private_span_low = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/span[1]/span[1]")))
						private_sale_low = private_span_low.text.split()[0]
						try:							
							private_span_high = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/span[3]/span[1]")))
							private_sale_high = private_span_hgih.text.split()[0]
						except TimeoutException as e:
							logging.error(e,exc_info=True)
					except TimeoutException as e:
						logging.error(e,exc_info=True)
				except TimeoutException as e:
					logging.error(e,exc_info=True)
				intents = discord.Intents.default()
				client = discord.Client(intents=intents)
				hpi_trade_low = span.text.split()[0]
				await message.channel.send("Evalutation for reg: " + registration)
				await message.channel.send("Trade low: " + hpi_trade_low)
				await message.channel.send("Trade high: " + hpi_trade_high)
				await message.channel.send("foreCourt_low: " + foreCourt_low)
				await message.channel.send("foreCourt_high" + foreCourt_high)
				await message.channel.send("private_sale_low" + private_sale_low)
				await message.channel.send("private_sale_high" + private_sale_high)
				driver.quit()
		except Exception as e:
			#await message.channel.send("Failed to get evaluation link")
			logging.error(e, exc_info=True)
			
	
