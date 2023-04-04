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
def current_time():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
info_statement = f"[INFO    {current_time()}]"
logging.basicConfig(filename='reg_bot_errors.log', level=logging.ERROR)
proxyManager = ProxyManager()
max_retry = 5
#-----------global settings

#-----------global variables
val_link = ''
hpi_span1_low_data = ''
hpi_span1_high_data = ''
hpi_span2_low_data = ''
hpi_span2_high_data = ''
hpi_span3_low_data = ''
hpi_span3_high_data = ''
foreCourt_low_data = ''
foreCourt_high_data = ''
private_low_data = ''
private_high_data = ''
hpi_span1_low = ''
#-----------global variables

#-----------Driver Settings
# drivers = [ChromeDriver, FirefoxDriver]
# selected_driver = random.choice(drivers)
# driverInstance = selected_driver.create()
# activeDriver = driverInstance.get_driver()
# activeDriver.quit()
# driver_info = f"[SELECTED DRIVER    {driverInstance}]"
#-----------Driver Settings

# print(f"{info_statement} {driver_info}")


async def or_less(message):
	intents = discord.Intents.default()
	client = discord.Client(intents=intents)
	try:
		cookies = WebDriverWait(activeDriver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#onetrust-accept-btn-handler")))
		cookies.click();
	except TimeoutException as e:
		logging.error(e,exc_info=True)
	try:
		global or_less_data
		or_less_span = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
		or_less_data = or_less_span.text
		formatted_or_less = f"Trade price: {or_less_data}"
	except TimeoutException as e:
		logging.error(e,exc_info=True)
	try:
		navforeCourt = WebDriverWait(activeDriver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[2]")))
		navforeCourt.click();
		try:
			raw_foreCourt_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
			foreCourt_price = raw_foreCourt_price.text.split()
			formatted_foreCourt_price = f"Forecourt Low: {foreCourt_price[0]} | High: {foreCourt_price[2]}"
		except TimeoutException as e:
			logging.error(e,exc_info=True)
	except TimeoutException as e:
		logging.error(e,exc_info=True)
	try:
		navprivate = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[1]")))
		navprivate.click();
		try:
			raw_private_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
			private_price = raw_private_price.text.split()
			formatted_private_price = f"Private Low: {private_price[0]} | High: {private_price[2]}"
		except TimeoutException as e:
			logging.error(e,exc_info=True)
	except TimeoutException as e:
		logging.error(e,exc_info=True)
	activeDriver.quit()
	await message.channel.send(formatted_or_less)
	await message.channel.send(formatted_foreCourt_price)
	await message.channel.send(formatted_private_price)


async def reg(message, registration, miles, activeDriver):
	fileManager = FileManager()
	randomManager = RandomManager()
	retry_counter = 0
	max_retry = 3
	while retry_counter < max_retry:
		proxy = proxyManager.get_random_proxy()
		ua = proxyManager.get_random_UA()
		try:
			activeDriver.get('https://hpivaluations.com')
			if "Free" in activeDriver.title:
				await message.channel.send("Connected to evaluation site. Stand by.")
				break  # exit loop if page loaded successfully
		except Exception as e:
			logging.error(e, exc_info=True)
			retry_counter += 1
			print(f"{timestamp} {info_statement} [Console]: Proxy connection failed: retrying. {retry_counter}")
			await message.channel.send("Retrying proxy..")
			proxyManager.remove_proxy(proxy)
			await asyncio.sleep(2)

	if retry_counter == max_retry:
		print(f"{timestamp} {info_statement} [console]: Maximum retries met while running !reg")
	else:
		await asyncio.sleep(10)
		try:
			# activeDriver.find_element((By.ID,'onetrust-button-group-parent'))
			# activeDriver.find_element((By.CLASS_NAME,'ot-sdk-three ot-sdk-columns has-reject-all-button'))
			cookies = WebDriverWait(activeDriver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#onetrust-accept-btn-handler")))
			cookies.click()
		except Exception as e:
			#await message.channel.send("Failed to accept cookes") 
			logging.error(e, exc_info=True)
		#enter reg
		await asyncio.sleep(2)
		try:
			enter_reg = WebDriverWait(activeDriver, 5).until(EC.element_to_be_clickable((By.XPATH,"//input[@placeholder='Enter Reg...']")))
			enter_reg.click();
			enter_reg.send_keys(registration)
			await asyncio.sleep(3)
			WebDriverWait(activeDriver, 7).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.icon.icon-navigateright'))).click();
		except Exception as e:
			#await message.channel.send("Failed to search. Error finding search button.")
			logging.error(e, exc_info=True)
		await asyncio.sleep(6)
		try:
			WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.XPATH,'//span[normalize-space()="I don\'t own this car"]'))).click();
			await asyncio.sleep(2)
			WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='hpiconsentCheckbox']"))).click();
			WebDriverWait(activeDriver,7).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='consentCheckbox']"))).click();
			await asyncio.sleep(2)
			WebDriverWait(activeDriver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='btn btn-primary radius js-modal-terms-cta']"))).click();
			await asyncio.sleep(2)
		except Exception as e:
			#await message.channel.send("Failed to declare ownership & accept terms")
			logging.error(e, exc_info=True)
		try:
			name = WebDriverWait(activeDriver,1).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='formName']")))
			name.click();
			await asyncio.sleep(5)
			name.send_keys(randomManager.create_hpi_name())
		except Exception as e:
			#await message.channel.send("Failed to enter name")
			logging.error(e, exc_info=True)
		try:
			email = WebDriverWait(activeDriver,1).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='formEmail']")))
			await asyncio.sleep(6)
			email.click();
			email.send_keys(randomManager.createEmail())
		except Exception as e:
			#await message.channel.send("Failed to enter email")
			logging.error(e, exc_info=True)
		try:
			postal = WebDriverWait(activeDriver,8).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='formPostcode']")))
			postal.click();
			await asyncio.sleep(5)
			postal.send_keys(randomManager.get_random_postCode())
		except Exception as e:
			#await message.channel.send("Failed to enter postcode")
			logging.error(e, exc_info=True)
		try:
			phone = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='formTelephone']")))
			phone.click();
			await asyncio.sleep(3)
			phone.send_keys(randomManager.random_phone())
		except Exception as e:
			#await message.channel.send("Failed to enter phone number")
			logging.error(e, exc_info=True)
		await message.channel.send("Getting report...")
		try:
			await asyncio.sleep(11)
			WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='btn btn-primary onboarding__btn onboarding__btn--next']"))).click();
			await asyncio.sleep(2)
			try:
				global hpi_span1_low
				hpi_span1_low = WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div/span[1]")))
			except TimeoutException as e:
				logging.error(e,exc_info=True)
			if not hpi_span1_low:
				activeDriver.quit()
				activeDriver = webdriver.ChromeOptions(options = driver_options)
				try:
					activeDriver.get('https://yopmail.com')
				except TimeoutException as e:
					logging.error(e, exc_info=True)							
				try:
					WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#accept"))).click();
				except TimeoutException as e:
					logging.error (e, exc_info=True)
				try:
					fileManager = FileManager()
					login=WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#login")))
					login.click()
					login.send_keys(fileManager.loademail())
					time.sleep(1)
					WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".material-icons-outlined.f36"))).click();
					iframe = activeDriver.find_element(By.ID,"ifmail")
					activeDriver.switch_to.frame(iframe)
					valuation = WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.XPATH,"//a[normalize-space()='View valuation']")))
					val_link = valuation.get_attribute("href")

				except Exception as e:
					#await message.channel.send("Failed to retrieve mailbox.")
					logging.error(e, exc_info=True)
				#get hpi_price 
				try:
					activeDriver.get(val_link)
					await asyncio.sleep(10)
					or_less_check = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
					check_or_less = or_less_check.text
#or less handler --------------------------------------------
					if "or less" in check_or_less:
						await or_less()
#or less handler end ----------------------------------------
					else:
						try:
							cookies = WebDriverWait(activeDriver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#onetrust-accept-btn-handler")))
							cookies.click();
							await asyncio.sleep(3)
						except TimeoutException as e:
							logging.error(e,exc_info=True)
#popup handler ----------------------------------------------
						await asyncio.sleep(15)
						try:
							no_button = WebDriverWait(activeDriver,2).until(EC.presence_of_element_located((By.XPATH,"/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/button[2]")))
							no_button.click();
						except TimeoutException as e:
							logging.error(e,exc_info=True)
#popup handler end ------------------------------------------
#mileage handler --------------------------------------------
						try:
							span_mileage = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/span[3]/span")))
							span_mileage.click();
							span_mileage_input = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div/div/input")))
							span_mileage_input.click();
							span_mileage_input.clear()
							span_mileage_input.send_keys(miles)
							span_mileage_submit = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div/button[2]")))
							span_mileage_submit.click();
							await asyncio.sleep(3)
						except TimeoutException as e:
							logging.error(e,exc_info=True)	
#mileage handler end ----------------------------------------			
						try:
							#milage counter
							global mileage_cnt
							global formatted_mileage
							milelage_str = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/span[3]")))
							mileage_cnt = milelage_str.text.split()
							formatted_mileage = f"Mileage for reg {registration} | {mileage_cnt[0]}"
						except TimeoutException as e:
							logging.error(e,exc_info=True)
						try:
							global good_price
							global formatted_trade_price
							raw_trade_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
							good_price = raw_trade_price.text.split("\n")
							formatted_trade_price = f"Trade good Low: {good_price[0]} | High: {good_price[2]} "
						except TimeoutException as e:
							logging.error(e,exc_info=True)
						try:
							await asyncio.sleep(5)
							navpoor = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a.ranger__label__item:nth-child(1)")))
							navpoor.click();
							try:
								global poor_price
								global formatted_poor_price
								raw_poor_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
								poor_price = raw_poor_price.text.split()
								formatted_poor_price = f"Trade poor Low: {poor_price[0]} | High: {poor_price[2]}"
							except TimeoutException as e:
								logging.error(e,exc_info=True)
						except TimeoutException as e:
							logging.error(e,exc_info=True)
						try:
							navbest = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/a[3]")))
							navbest.click();
							try:
								global best_price
								global formatted_best_price
								raw_best_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
								best_price = raw_best_price.text.split()
								formatted_best_price = f"Trade best Low: {best_price[0]} | High: {best_price[2]}"
							except TimeoutException as e:
								logging.error(e,exc_info=True)
						except TimeoutException as e:
							logging.error(e,exc_info=True)
						try:
							navforeCourt = WebDriverWait(activeDriver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[2]")))
							navforeCourt.click();
							try:
								global foreCourt_price
								global formatted_foreCourt_price
								raw_foreCourt_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
								foreCourt_price = raw_foreCourt_price.text.split()
								formatted_foreCourt_price = f"Forecourt Low: {foreCourt_price[0]} | High: {foreCourt_price[2]}"
							except TimeoutException as e:
								logging.error(e,exc_info=True)
						except TimeoutException as e:
							logging.error(e,exc_info=True)
						try:
							navprivate = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[1]")))
							navprivate.click();
							try:
								global private_price
								global formatted_private_price
								raw_private_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
								private_price = raw_private_price.text.split()
								formatted_private_price = f"Private: {private_price[0]} | High: {private_price[2]}"
							except TimeoutException as e:
								logging.error(e,exc_info=True)
						except TimeoutException as e:
							logging.error(e,exc_info=True)
						intents = discord.Intents.default()
						client = discord.Client(intents=intents)
						await message.channel.send(formatted_mileage)
						await message.channel.send("------------------------------------")
						await message.channel.send(formatted_poor_price)
						await message.channel.send(formatted_trade_price)
						await message.channel.send(formatted_best_price)
						await message.channel.send("------------------------------------")
						await message.channel.send(formatted_private_price)
						await message.channel.send("------------------------------------")
						await message.channel.send(formatted_foreCourt_price)
						activeDriver.quit()
				except Exception as e:
					logging.error(e,exc_info=True)
			else:
				await asyncio.sleep(2)
				or_less_check = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
				check_or_less = or_less_check.text
				if "or less" in check_or_less:
					await or_less(message)
				else:
					try:
						cookies = WebDriverWait(activeDriver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#onetrust-accept-btn-handler")))
						cookies.click();
					except TimeoutException as e:
						logging.error(e,exc_info=True)
#popup handler ----------------------------------------------
					await asyncio.sleep(15)
					try:
						no_button = WebDriverWait(activeDriver,2).until(EC.presence_of_element_located((By.XPATH,"/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/button[2]")))
						no_button.click();
					except TimeoutException as e:
						logging.error(e,exc_info=True)
#popup handler end ------------------------------------------
					try:
						span_mileage = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/span[3]/span")))
						span_mileage.click();
						span_mileage_input = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div/div/input")))
						span_mileage_input.click();
						span_mileage_input.clear()
						span_mileage_input.send_keys(miles)
						span_mileage_submit = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div/button[2]")))
						span_mileage_submit.click();
						await asyncio.sleep(3)
					except TimeoutException as e:
						logging.error(e,exc_info=True)	
					try:
						#milage counter
						milelage_str = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/span[3]")))
						mileage_cnt = milelage_str.text.split()
						formatted_mileage = f"Mileage for reg {registration} | {mileage_cnt[0]}"
					except TimeoutException as e:
						logging.error(e,exc_info=True)						
					try:
						raw_trade_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
						good_price = raw_trade_price.text.split("\n")
						formatted_trade_price = f"Trade good Low: {good_price[0]} | High: {good_price[2]} "
					except TimeoutException as e:
						logging.error(e,exc_info=True)
					try:
						await asyncio.sleep(5)
						navpoor = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/a[1]")))
						navpoor.click();
						try:
							raw_poor_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
							poor_price = raw_poor_price.text.split()
							formatted_poor_price = f"Trade poor Low: {poor_price[0]} | High: {poor_price[2]}"
						except TimeoutException as e:
							logging.error(e,exc_info=True)
					except TimeoutException as e:
						logging.error(e,exc_info=True)
					try:
						navbest = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/a[3]")))
						navbest.click();
						try:
							raw_best_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
							best_price = raw_best_price.text.split()
							formatted_best_price = f"Trade best Low: {best_price[0]} | High: {best_price[2]}"
						except TimeoutException as e:
							logging.error(e,exc_info=True)
					except TimeoutException as e:
						logging.error(e,exc_info=True)
					try:
						navforeCourt = WebDriverWait(activeDriver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[2]")))
						navforeCourt.click();
						try:
							raw_foreCourt_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
							foreCourt_price = raw_foreCourt_price.text.split()
							formatted_foreCourt_price = f"Forecourt Low: {foreCourt_price[0]} | High: {foreCourt_price[2]}"
						except TimeoutException as e:
							logging.error(e,exc_info=True)
					except TimeoutException as e:
						logging.error(e,exc_info=True)
					try:
						navprivate = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[1]")))
						navprivate.click();
						try:
							raw_private_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
							private_price = raw_private_price.text.split()
							formatted_private_price = f"Private Low: {private_price[0]} | High: {private_price[2]}"
						except TimeoutException as e:
							logging.error(e,exc_info=True)
					except TimeoutException as e:
						logging.error(e,exc_info=True)
					intents = discord.Intents.default()
					client = discord.Client(intents=intents)
					await message.channel.send(formatted_mileage)
					await message.channel.send("------------------------------------")
					await message.channel.send(formatted_poor_price)
					await message.channel.send(formatted_trade_price)
					await message.channel.send(formatted_best_price)
					await message.channel.send("------------------------------------")
					await message.channel.send(formatted_private_price)
					await message.channel.send("------------------------------------")
					await message.channel.send(formatted_foreCourt_price)
					activeDriver.quit()
		except Exception as e:
			#await message.channel.send("Failed to get evaluation link")
			logging.error(e, exc_info=True)

async def reg_nomiles(message, registration, activeDriver):
	fileManager = FileManager()
	randomManager = RandomManager()
	retry_counter = 0
	max_retry = 3
	while retry_counter < max_retry:
		proxy = proxyManager.get_random_proxy()
		ua = proxyManager.get_random_UA()
		try:
			activeDriver.get('https://hpivaluations.com')
			if "Free" in activeDriver.title:
				await message.channel.send("Connected to evaluation site. Stand by.")
				break  # exit loop if page loaded successfully
		except Exception as e:
			logging.error(e, exc_info=True)
			retry_counter += 1
			print(f"{timestamp} {info_statement} [Console]: Proxy connection failed: retrying. {retry_counter}")
			await message.channel.send("Retrying proxy..")
			proxyManager.remove_proxy(proxy)
			await asyncio.sleep(2)

	if retry_counter == max_retry:
		print(f"{timestamp} {info_statement} [console]: Maximum retries met while running !reg")
	else:
		await asyncio.sleep(10)
		try:
			# activeDriver.find_element((By.ID,'onetrust-button-group-parent'))
			# activeDriver.find_element((By.CLASS_NAME,'ot-sdk-three ot-sdk-columns has-reject-all-button'))
			cookies = WebDriverWait(activeDriver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#onetrust-accept-btn-handler")))
			cookies.click()
		except Exception as e:
			#await message.channel.send("Failed to accept cookes") 
			logging.error(e, exc_info=True)
		#enter reg
		await asyncio.sleep(2)
		try:
			enter_reg = WebDriverWait(activeDriver, 5).until(EC.element_to_be_clickable((By.XPATH,"//input[@placeholder='Enter Reg...']")))
			enter_reg.click();
			enter_reg.send_keys(registration)
			await asyncio.sleep(3)
			WebDriverWait(activeDriver, 7).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.icon.icon-navigateright'))).click();
		except Exception as e:
			#await message.channel.send("Failed to search. Error finding search button.")
			logging.error(e, exc_info=True)
		await asyncio.sleep(6)
		try:
			WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.XPATH,'//span[normalize-space()="I don\'t own this car"]'))).click();
			await asyncio.sleep(2)
			WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='hpiconsentCheckbox']"))).click();
			WebDriverWait(activeDriver,7).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='consentCheckbox']"))).click();
			await asyncio.sleep(2)
			WebDriverWait(activeDriver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='btn btn-primary radius js-modal-terms-cta']"))).click();
			await asyncio.sleep(2)
		except Exception as e:
			#await message.channel.send("Failed to declare ownership & accept terms")
			logging.error(e, exc_info=True)
		try:
			name = WebDriverWait(activeDriver,1).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='formName']")))
			name.click();
			await asyncio.sleep(5)
			name.send_keys(randomManager.create_hpi_name())
		except Exception as e:
			#await message.channel.send("Failed to enter name")
			logging.error(e, exc_info=True)
		try:
			email = WebDriverWait(activeDriver,1).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='formEmail']")))
			await asyncio.sleep(6)
			email.click();
			email.send_keys(randomManager.createEmail())
		except Exception as e:
			#await message.channel.send("Failed to enter email")
			logging.error(e, exc_info=True)
		try:
			postal = WebDriverWait(activeDriver,8).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='formPostcode']")))
			postal.click();
			await asyncio.sleep(5)
			postal.send_keys(randomManager.get_random_postCode())
		except Exception as e:
			#await message.channel.send("Failed to enter postcode")
			logging.error(e, exc_info=True)
		try:
			phone = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='formTelephone']")))
			phone.click();
			await asyncio.sleep(3)
			phone.send_keys(randomManager.random_phone())
		except Exception as e:
			#await message.channel.send("Failed to enter phone number")
			logging.error(e, exc_info=True)
		await message.channel.send("Getting report...")
		try:
			await asyncio.sleep(11)
			WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='btn btn-primary onboarding__btn onboarding__btn--next']"))).click();
			await asyncio.sleep(2)
			try:
				global hpi_span1_low
				hpi_span1_low = WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div/span[1]")))
			except TimeoutException as e:
				logging.error(e,exc_info=True)
			if not hpi_span1_low:
				activeDriver.quit()
				activeDriver = webdriver.ChromeOptions(options = driver_options)
				try:
					activeDriver.get('https://yopmail.com')
				except TimeoutException as e:
					logging.error(e, exc_info=True)							
				try:
					WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#accept"))).click();
				except TimeoutException as e:
					logging.error (e, exc_info=True)
				try:
					fileManager = FileManager()
					login=WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#login")))
					login.click()
					login.send_keys(fileManager.loademail())
					time.sleep(1)
					WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".material-icons-outlined.f36"))).click();
					iframe = activeDriver.find_element(By.ID,"ifmail")
					activeDriver.switch_to.frame(iframe)
					valuation = WebDriverWait(activeDriver,5).until(EC.element_to_be_clickable((By.XPATH,"//a[normalize-space()='View valuation']")))
					val_link = valuation.get_attribute("href")

				except Exception as e:
					#await message.channel.send("Failed to retrieve mailbox.")
					logging.error(e, exc_info=True)
				#get hpi_price 
				try:
					activeDriver.get(val_link)
					await asyncio.sleep(10)
					or_less_check = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
					check_or_less = or_less_check.text
#or less handler --------------------------------------------
					if "or less" in check_or_less:
						await or_less()
#or less handler end ----------------------------------------
					else:
						try:
							cookies = WebDriverWait(activeDriver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#onetrust-accept-btn-handler")))
							cookies.click();
							await asyncio.sleep(3)
						except TimeoutException as e:
							logging.error(e,exc_info=True)
#popup handler ----------------------------------------------
						await asyncio.sleep(15)
						try:
							no_button = WebDriverWait(activeDriver,2).until(EC.presence_of_element_located((By.XPATH,"/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/button[2]")))
							no_button.click();
						except TimeoutException as e:
							logging.error(e,exc_info=True)
#popup handler end ------------------------------------------			
						try:
							#milage counter
							global mileage_cnt
							global formatted_mileage
							milelage_str = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/span[3]")))
							mileage_cnt = milelage_str.text.split()
							formatted_mileage = f"Mileage for reg {registration} | {mileage_cnt[0]}"
						except TimeoutException as e:
							logging.error(e,exc_info=True)
						try:
							global good_price
							global formatted_trade_price
							raw_trade_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
							good_price = raw_trade_price.text.split("\n")
							formatted_trade_price = f"Trade good Low: {good_price[0]} | High: {good_price[2]} "
						except TimeoutException as e:
							logging.error(e,exc_info=True)
						try:
							await asyncio.sleep(5)
							navpoor = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a.ranger__label__item:nth-child(1)")))
							navpoor.click();
							try:
								global poor_price
								global formatted_poor_price
								raw_poor_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
								poor_price = raw_poor_price.text.split()
								formatted_poor_price = f"Trade poor Low: {poor_price[0]} | High: {poor_price[2]}"
							except TimeoutException as e:
								logging.error(e,exc_info=True)
						except TimeoutException as e:
							logging.error(e,exc_info=True)
						try:
							navbest = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/a[3]")))
							navbest.click();
							try:
								global best_price
								global formatted_best_price
								raw_best_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
								best_price = raw_best_price.text.split()
								formatted_best_price = f"Trade best Low: {best_price[0]} | High: {best_price[2]}"
							except TimeoutException as e:
								logging.error(e,exc_info=True)
						except TimeoutException as e:
							logging.error(e,exc_info=True)
						try:
							navforeCourt = WebDriverWait(activeDriver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[2]")))
							navforeCourt.click();
							try:
								global foreCourt_price
								global formatted_foreCourt_price
								raw_foreCourt_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
								foreCourt_price = raw_foreCourt_price.text.split()
								formatted_foreCourt_price = f"Forecourt Low: {foreCourt_price[0]} | High: {foreCourt_price[2]}"
							except TimeoutException as e:
								logging.error(e,exc_info=True)
						except TimeoutException as e:
							logging.error(e,exc_info=True)
						try:
							navprivate = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[1]")))
							navprivate.click();
							try:
								global private_price
								global formatted_private_price
								raw_private_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
								private_price = raw_private_price.text.split()
								formatted_private_price = f"Private: {private_price[0]} | High: {private_price[2]}"
							except TimeoutException as e:
								logging.error(e,exc_info=True)
						except TimeoutException as e:
							logging.error(e,exc_info=True)
						intents = discord.Intents.default()
						client = discord.Client(intents=intents)
						await message.channel.send(formatted_mileage)
						await message.channel.send("------------------------------------")
						await message.channel.send(formatted_poor_price)
						await message.channel.send(formatted_trade_price)
						await message.channel.send(formatted_best_price)
						await message.channel.send("------------------------------------")
						await message.channel.send(formatted_private_price)
						await message.channel.send("------------------------------------")
						await message.channel.send(formatted_foreCourt_price)
						activeDriver.quit()
				except Exception as e:
					logging.error(e,exc_info=True)
			else:
				await asyncio.sleep(2)
				or_less_check = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
				check_or_less = or_less_check.text
				if "or less" in check_or_less:
					await or_less(message)
				else:
					try:
						cookies = WebDriverWait(activeDriver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#onetrust-accept-btn-handler")))
						cookies.click();
					except TimeoutException as e:
						logging.error(e,exc_info=True)
#popup handler ----------------------------------------------
					await asyncio.sleep(15)
					try:
						no_button = WebDriverWait(activeDriver,2).until(EC.presence_of_element_located((By.XPATH,"/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/button[2]")))
						no_button.click();
					except TimeoutException as e:
						logging.error(e,exc_info=True)
#popup handler end ------------------------------------------	
					try:
						#milage counter
						milelage_str = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/span[3]")))
						mileage_cnt = milelage_str.text.split()
						formatted_mileage = f"Mileage for reg {registration} | {mileage_cnt[0]}"
					except TimeoutException as e:
						logging.error(e,exc_info=True)						
					try:
						raw_trade_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
						good_price = raw_trade_price.text.split("\n")
						formatted_trade_price = f"Trade good Low: {good_price[0]} | High: {good_price[2]} "
					except TimeoutException as e:
						logging.error(e,exc_info=True)
					try:
						await asyncio.sleep(5)
						navpoor = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/a[1]")))
						navpoor.click();
						try:
							raw_poor_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
							poor_price = raw_poor_price.text.split()
							formatted_poor_price = f"Trade poor Low: {poor_price[0]} | High: {poor_price[2]}"
						except TimeoutException as e:
							logging.error(e,exc_info=True)
					except TimeoutException as e:
						logging.error(e,exc_info=True)
					try:
						navbest = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/a[3]")))
						navbest.click();
						try:
							raw_best_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
							best_price = raw_best_price.text.split()
							formatted_best_price = f"Trade best Low: {best_price[0]} | High: {best_price[2]}"
						except TimeoutException as e:
							logging.error(e,exc_info=True)
					except TimeoutException as e:
						logging.error(e,exc_info=True)
					try:
						navforeCourt = WebDriverWait(activeDriver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[2]")))
						navforeCourt.click();
						try:
							raw_foreCourt_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
							foreCourt_price = raw_foreCourt_price.text.split()
							formatted_foreCourt_price = f"Forecourt Low: {foreCourt_price[0]} | High: {foreCourt_price[2]}"
						except TimeoutException as e:
							logging.error(e,exc_info=True)
					except TimeoutException as e:
						logging.error(e,exc_info=True)
					try:
						navprivate = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[1]")))
						navprivate.click();
						try:
							raw_private_price = WebDriverWait(activeDriver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
							private_price = raw_private_price.text.split()
							formatted_private_price = f"Private Low: {private_price[0]} | High: {private_price[2]}"
						except TimeoutException as e:
							logging.error(e,exc_info=True)
					except TimeoutException as e:
						logging.error(e,exc_info=True)
					intents = discord.Intents.default()
					client = discord.Client(intents=intents)
					await message.channel.send(formatted_mileage)
					await message.channel.send("------------------------------------")
					await message.channel.send(formatted_poor_price)
					await message.channel.send(formatted_trade_price)
					await message.channel.send(formatted_best_price)
					await message.channel.send("------------------------------------")
					await message.channel.send(formatted_private_price)
					await message.channel.send("------------------------------------")
					await message.channel.send(formatted_foreCourt_price)
					activeDriver.quit()
		except Exception as e:
			#await message.channel.send("Failed to get evaluation link")
			logging.error(e, exc_info=True)
	