import time
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import InvalidArgumentException
import asyncio

logging.basicConfig(filename='errors.log', level=logging.ERROR)
options = webdriver.ChromeOptions()
# Adding argument to disable the AutomationControlled flag 
options.add_argument("--disable-blink-features=AutomationControlled") 
 
# Exclude the collection of enable-automation switches 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
 
# Turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False) 
 
# Setting the driver path and requesting a page 
driver = webdriver.Chrome(options=options) 
 
# Changing the property of the navigator value for webdriver to undefined 
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

driver = webdriver.Chrome(options = options)

trade_price = ''

async def get_values():
	# driver.get("https://hpivaluations.com/report/view/VA25424604-PE06XYV")
	driver.get("https://hpivaluations.com/report/view/VA25409334-FJ19RSV")
	await asyncio.sleep(10)
	or_less_check = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
	check_or_less = or_less_check.text
	if "or less" in check_or_less:
		await or_less()
	else:
		try:
			cookies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#onetrust-accept-btn-handler")))
			cookies.click();
		except TimeoutException as e:
			logging.error(e,exc_info=True)
		#edit mileage
		await asyncio.sleep(15)
		try:
			no_button = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,"/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/button[2]")))
			no_button.click();
		except TimeoutException as e:
			logging.error(e,exc_info=True)
		try:
			span_mileage = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/span[3]/span")))
			span_mileage.click();
			span_mileage_input = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div/div/input")))
			span_mileage_input.click();
			span_mileage_input.clear()
			span_mileage_input.send_keys("60000")
			span_mileage_submit = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div/button[2]")))
			span_mileage_submit.click();
		except TimeoutException as e:
			logging.error(e,exc_info=True)
		try:
			#milage counter
			global mileage_cnt
			global formatted_mileage
			milelage_str = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/span[3]")))
			mileage_cnt = milelage_str.text.split()
			formatted_mileage = f"Mileage | {mileage_cnt[0]}"
		except TimeoutException as e:
			logging.error(e,exc_info=True)
		try:
			global good_price
			global formatted_trade_price
			raw_trade_price = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
			good_price = raw_trade_price.text.split("\n")
			formatted_trade_price = f"Trade good low: {good_price[0]} | Trade good high: {good_price[2]} "
		except TimeoutException as e:
			logging.error(e,exc_info=True)
		try:
			await asyncio.sleep(5)
			#navpoor = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/a[1]")))
			navpoor = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a.ranger__label__item:nth-child(1)")))
			navpoor.click();
			try:
				global poor_price
				global formatted_poor_price
				raw_poor_price = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
				poor_price = raw_poor_price.text.split()
				formatted_poor_price = f"Trade poor low: {poor_price[0]} | Trade poor high: {poor_price[2]}"
			except TimeoutException as e:
				logging.error(e,exc_info=True)
		except TimeoutException as e:
			logging.error(e,exc_info=True)
		try:
			navbest = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/a[3]")))
			navbest.click();
			try:
				global best_price
				global formatted_best_price
				raw_best_price = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
				best_price = raw_best_price.text.split()
				formatted_best_price = f"Trade best low: {best_price[0]} | Trade best high: {best_price[2]}"
			except TimeoutException as e:
				logging.error(e,exc_info=True)
		except TimeoutException as e:
			logging.error(e,exc_info=True)
		try:
			navforeCourt = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[2]")))
			navforeCourt.click();
			try:
				global foreCourt_price
				global formatted_foreCourt_price
				raw_foreCourt_price = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
				foreCourt_price = raw_foreCourt_price.text.split()
				formatted_foreCourt_price = f"Forecourt Low: {foreCourt_price[0]} | Forecourt High: {foreCourt_price[2]}"
			except TimeoutException as e:
				logging.error(e,exc_info=True)
		except TimeoutException as e:
			logging.error(e,exc_info=True)
		try:
			navprivate = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[1]")))
			navprivate.click();
			try:
				global private_price
				global formatted_private_price
				raw_private_price = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
				private_price = raw_private_price.text.split()
				formatted_private_price = f"Private Low: {private_price[0]} | Private High: {private_price[2]}"
			except TimeoutException as e:
				logging.error(e,exc_info=True)
		except TimeoutException as e:
			logging.error(e,exc_info=True)
		print(formatted_poor_price)
		print(formatted_trade_price)
		print(formatted_best_price)
		print(formatted_private_price)
		print(formatted_foreCourt_price)
		# await message.channel.send(formatted_poor_price)
		# await message.channel.send(formatted_trade_price)
		# await message.channel.send(formatted_best_price)

async def or_less():
	try:
		cookies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#onetrust-accept-btn-handler")))
		cookies.click();
	except TimeoutException as e:
		logging.error(e,exc_info=True)
	try:
		global or_less_data
		or_less_span = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
		or_less_data = or_less_span.text
	except TimeoutException as e:
		logging.error(e,exc_info=True)
		try:
			navforeCourt = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[2]")))
			navforeCourt.click();
			try:
				raw_foreCourt_price = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
				foreCourt_price = raw_foreCourt_price.text.split()
				formatted_foreCourt_price = f"Forecourt Low: {foreCourt_price[0]} | Forecourt High: {foreCourt_price[2]}"
			except TimeoutException as e:
				logging.error(e,exc_info=True)
		except TimeoutException as e:
			logging.error(e,exc_info=True)
		try:
			navprivate = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[1]")))
			navprivate.click();
			try:
				raw_private_price = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]")))
				private_price = raw_private_price.text.split()
				formatted_private_price = f"Private Low: {private_price[0]} | Private High: {private_price[2]}"
			except TimeoutException as e:
				logging.error(e,exc_info=True)
		except TimeoutException as e:
			logging.error(e,exc_info=True)
	print(or_less_data)

asyncio.run(get_values())
