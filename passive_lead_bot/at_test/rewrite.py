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

#-----------selenium settings
driver_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options = driver_options) #- initialize instance
driver.quit() #- close initial instance
#-----------selenium settings

class randoms:
	def __init__(self):
		pass

	def ranFName(self):
		with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\names.txt","r") as f:
			first = f.readlines()
		return random.choice(first).strip()

	def ranLName(self):
		with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\names.txt","r") as f:
			last = f.readlines()
		return random.choice(last).strip()

	def randomEmail_name(self):
	    with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\names.txt", "r") as f:
	        names = f.readlines()
	    return random.choice(names).strip()

	def random_postCode(self):
		with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\postcode.txt","r") as f:
			postcode = f.readlines()
		return random.choice(postcode).strip()


	def hpi_name(self):
		with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\names.txt","r") as f:
			names = f.readlines()
		name = random.choice(names).strip()
		return name[:len(name)//2]+" "+name[len(name)//2]

	def random_phone(self):
		phone_suffix = str(random.randint(0,999999999)).zfill(9)
		phone_number= "07"+phone_suffix
		return phone_number

	def random_address(self):
	    with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\addresses.txt","r") as f:
	        addresses = f.readlines()
	        ranAdd = random.choice(addresses).strip('"\n')
	    street_town, postcode = ranAdd.rsplit(',',1)
	    town = street_town.rsplit(',',1)[-1].strip()
	    street = street_town.rsplit(',',1)[0].strip()
	    houseNo = street.split()[0].strip()
	    return houseNo, street, town, postcode

	def createEmail(self):
		global ranEmail
		ranEmail = self.randomEmail_name()+"."+self.random_phone()+"@prc.cx"
		with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\email.txt","w") as f:
			f.write(ranEmail)
			f.close()
		return ranEmail
# for reference
ranDom = randoms()
# print(ranDom.ranFName())
# print(ranDom.ranLName())
# print(ranDom.random_postCode())
# print(ranDom.hpi_name())
# print(ranDom.random_phone())
# print(ranDom.random_address())
# print(ranDom.createEmail())
###############################


#------- finance handler start  -------#
async def finance_handler():
	await asyncio.sleep(5)
	try:
		#ok lets go button
		WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/button[1]"))).click();
		try:
			WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/label[1]/span[1]"))).click();
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("what is `gender`")
		try:
			f_Name = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]")))
			f_Name.click();
			f_Name.send_keys(ranDom.ranFName())
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("Failed to enter `f_Name`")
		try:
			l_Name = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/input[1]")))
			l_Name.click();
			l_Name.send_keys(ranDom.ranLName())
			WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[1]/div[1]/div[3]/button[1]/div[1]"))).click();
			await asyncio.sleep(1)
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("Failed to enter `l_Name`")
		try:
			dd = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[5]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]")))
			dd.click();
			dd.send_keys(random.randint(1,20))
			mm = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[5]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/input[1]")))
			mm.click();
			mm.send_keys("05")
			yy = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[5]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/input[1]")))
			yy.click();
			# print("Max Length:", yy.get_attribute("maxlength"))
			yy.send_keys(1,1996)
			WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[5]/div[2]/div[1]/div[1]/div[4]/button[1]/div[1]"))).click();
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("Error with DoB DD handling")
		try:
			relStatus = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[6]/div[2]/div[1]/div[1]/label[1]/span[1]")))
			relStatus.click();
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("Failed to .click(); `relStatus`")
		try:
			income = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[7]/div[2]/div[1]/div[1]/div[1]/input[1]")))
			income.click();
			income.send_keys(random.randint(0,100000))
			WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[7]/div[2]/div[1]/button[1]"))).click();
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("failed to enter `income`")
		try:
			dl = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[8]/div[2]/div[1]/div[1]/label[1]/span[1]")))
			dl.click();
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("failed to submit `dl` status")
		try:
			address = ranDom.random_address()
			houseNo = address[0]
			street = address[1]
			town = address[2]
			postcode = address[3]
			driver.execute_script("window.scrollTo(0, 300)")
			try:
				_postcode = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[9]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]")))
				_postcode.click();
				_postcode.send_keys(postcode)
				WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[9]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/button[1]"))).click();
			except TimeoutException as e:
				logging.error(e, exc_info=True)
				#await message.channel.send("Failed to send `postcode(1)`")
			try:
				await asyncio.sleep(1)
				WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[9]/div[1]/div[2]/div[1]/div[1]/div[2]/a[1]"))).click();
				house_number = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[9]/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/input[1]")))
				house_number.click();
				house_number.send_keys(houseNo)
			except TimeoutException as e:
				logging.error(e, exc_info=True)
				#await message.channel.send("Failed to enter `houseNo`")
			try:
				__street = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[9]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/input[1]")))
				__street.click();
				__street.send_keys(street)
			except TimeoutException as e:
				logging.error(e, exc_info=True)
				#await message.channel.send("failed to enter `street`")
			try:
				__town = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[9]/div[1]/div[3]/div[1]/div[2]/div[3]/div[1]/input[1]")))
				__town.click();
				__town.send_keys(town)
				WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[9]/div[1]/div[3]/div[1]/div[2]/div[6]/button[1]/div[1]"))).click();
			except TimeoutException as e:
				logging.error(e, exc_info=True)
				#await message.channel.send("failed to input `town`")
			await asyncio.sleep(2)
			# try:
			# 	__postcode = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[9]/div[1]/div[3]/div[1]/div[2]/div[5]/div[1]/input[1]")))
			# 	__postcode.click();
			# 	__postcode.send_keys(postcode)
			# except TimeoutException:
			# 	print("Failed to enter postcode(2)")
			try:
				__yy = WebDriverWait(driver,4).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[9]/div[1]/div[4]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]")))
				__yy.click();
				__yy.send_keys(15)
				__mm = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[9]/div[1]/div[4]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/input[1]")))
				__mm.click();
				__mm.send_keys(7)
				WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[9]/div[1]/div[4]/div[2]/div[1]/div[1]/div[3]/button[1]"))).click();
			except TimeoutException as e:
				logging.error(e, exc_info=True)
				#await message.channel.send("failed to enter `time_at_address`")
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("faled to handle `address input`")
		try:
			home_owner = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[9]/div[1]/div[5]/div[2]/div[1]/div[1]/label[1]/span[1]")))
			home_owner.click()
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			print("Failed `home_owner`")
		try:
			self_employed = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[10]/div[1]/div[1]/div[2]/div[1]/div[1]/label[2]/span[1]")))
			self_employed.click();
			job_title = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[10]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/input[1]")))
			job_title.click();
			job_title.send_keys("CIS")
			WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[10]/div[1]/div[2]/div[2]/div[1]/button[1]/div[1]"))).click();
			myself = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[10]/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/input[1]")))
			myself.click();
			myself.send_keys("myself")
			WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[10]/div[1]/div[3]/div[2]/div[1]/button[1]/div[1]"))).click();
			work_loc = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[10]/div[1]/div[4]/div[2]/div[1]/div[1]/div[1]/input[1]")))
			work_loc.click();
			work_loc.send_keys(town)
			WebDriverWait(driver,4).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[10]/div[1]/div[4]/div[2]/div[1]/button[1]/div[1]"))).click();
			how_long_yy = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[10]/div[1]/div[5]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]")))
			how_long_yy.click();
			how_long_yy.send_keys(4)
			how_long_mm = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[10]/div[1]/div[5]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/input[1]")))
			# how_long_mm.click();
			# how_long_yy.send_keys(7)
			WebDriverWait(driver,4).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[10]/div[1]/div[5]/div[2]/div[1]/div[1]/div[3]/button[1]"))).click();
			await asyncio.sleep(1)
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("Failed to enter `employment_details`")
		try:
			ranEmail = ranDom.randomEmail_name()+"@prc.cx"
			enter_email = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[11]/div[2]/div[1]/div[1]/div[1]/input[1]")))
			enter_email.click();
			enter_email.send_keys(ranEmail)
			# print(ranEmail)
			WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[11]/div[2]/div[1]/button[1]"))).click();
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("Failed to `enter_email`")
		try:
			await asyncio.sleep(1)
			phoneNo = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[12]/div[2]/div[1]/div[1]/div[1]/input[1]")))
			phoneNo.click()
			phoneNo.send_keys(random_phone())
			WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[12]/div[2]/div[1]/button[1]/div[1]"))).click();
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("Failed to enter `phoneNo`")
		try:
			contact_email = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[13]/div[2]/div[1]/div[1]/div[1]/div[1]/label[1]/span[1]")))
			contact_email.click();
			WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[13]/div[2]/div[1]/div[1]/div[2]/button[1]/div[1]"))).click();
			await asyncio.sleep(2)
			WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[15]/div[2]/button[1]"))).click();
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("Failed to `contact_email` `go`")
		try:
			password = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]/input[1]")))
			password.click();
			password.send_keys("ThisIsAPassword1234!!")
			WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[3]/main[1]/div[1]/div[1]/div[1]/form[1]/div[2]/button[1]"))).click();
			await asyncio.sleep(5)
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("Failed to enter `password`")
		try:
			find_nplate_P = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[4]/div[2]/div[1]/div[2]/div[1]/p[2]")))
			global nplate
			nplate = find_nplate_P.text.split()[-1]
			with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\reg.txt","a") as f:
				f.write(nplate+"\n")
			#await message.channel.send(nplate)
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("failed to find `nplate`")
	except TimeoutException as e:
		now = datetime.datetime.now()
		timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
		print(f"[{timestamp}] {info_statement} [Console]: Failed to start the finance process after finding finance_option")
		logging.error(e,exc_info=True)
		#failed to start finance handler

#------- finance handler end -------#









#------- HPI Valuations handler start -------#
async def getHPI(leads_channel):
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
			await asyncio.sleep(2)
			try:
				span_mileage = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/span[3]/span")))
				span_mileage.click();
				span_mileage_input = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div/div/input")))
				span_mileage_input.click();
				span_mileage_input.clear()
				span_mileage_input.send_keys(miles)
				span_mileage_submit = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div/button[2]")))
				span_mileage_submit.click();
				await asyncio.sleep(3)
			except TimeoutException as e:
				logging.error(e,exc_info=True)						
			try:
				#milage counter
				global mileage_cnt
				global formatted_mileage
				milelage_str = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/span[3]")))
				mileage_cnt = milelage_str.text.split()
				formatted_mileage = f"Mileage for reg {registration} | High: {mileage_cnt[0]}"
			except TimeoutException as e:
				logging.error(e,exc_info=True)
			try:
				global good_price
				global formatted_trade_price
				raw_trade_price = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
				good_price = raw_trade_price.text.split("\n")
				formatted_trade_price = f"Trade good Low: {good_price[0]} | High: {good_price[2]} "
			except TimeoutException as e:
				logging.error(e,exc_info=True)
			try:
				navpoor = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/a[1]")))
				navpoor.click();
				try:
					global poor_price
					global formatted_poor_price
					raw_poor_price = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div")))
					poor_price = raw_poor_price.text.split()
					formatted_poor_price = f"Trade poor Low: {poor_price[0]} | High: {poor_price[2]}"
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
					formatted_best_price = f"Trade best Low: {best_price[0]} | High: {best_price[2]}"
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
					formatted_foreCourt_price = f"Forecourt Low: {foreCourt_price[0]} | High: {foreCourt_price[2]}"
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
					formatted_private_price = f"Private: {private_price[0]} | High: {private_price[2]}"
				except TimeoutException as e:
					logging.error(e,exc_info=True)
			except TimeoutException as e:
				logging.error(e,exc_info=True)
			intents = discord.Intents.default()
			client = discord.Client(intents=intents)
			await leads_channel.send("--------------NEW LEAD--------------")
			await leads_channel.send(formatted_mileage)
			await leads_channel.send("------------------------------------")
			await leads_channel.send(formatted_poor_price)
			await leads_channel.send(formatted_trade_price)
			await leads_channel.send(formatted_best_price)
			await leads_channel.send("------------------------------------")
			await leads_channel.send(formatted_private_price)
			await leads_channel.send("------------------------------------")
			await leads_channel.send(formatted_foreCourt_price)
			await leads_channel.send("------------------------------------")
			await leads_channel.send(auto_trader_url)
			driver.quit()
	except Exception as e:
		logging.error(e,exc_info=True)
#------- HPI Valuations handler end -------#






#------- Listing handler start -------#
async def getListings():
	now = datetime.datetime.now()
	timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
	retry_counter = 0
	max_retry = 3
	while retry_counter < max_retry:
		print(f"[{timestamp}] {info_statement} [Console]: Started scrape.")
		with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\proxy.txt") as f:
			proxies = f.readlines()
			proxy = random.choice(proxies).strip()
		# with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\user-agents.txt") as f:
		# 	user_agents = f.readlines()
		# 	user_agent = random.choice(user_agents).strip()
		driver_options.add_argument("--proxy-server=http://"+proxy)
		#driver_options.add_argument("--user-agent="+user_agent)
		driver_options.add_argument("--start-maximized")
		driver = webdriver.Chrome(options = driver_options)
		try:
			driver.get("https://autotrader.co.uk")
			if "Free" in driver.title:
				break  # exit loop if page loaded successfully
		except Exception as e:
			logging.error(e,exc_info=True)
			retry_counter = retry_counter+1
			await asyncio.sleep(2)
	# wait for page to load
	await asyncio.sleep(2)
	if retry_counter == max_retry:
		now = datetime.datetime.now()
		timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
		print(f"{timestamp} {info_statement} [console]: Maximum retries met while running startScrape")
	else:
		try:
			await asyncio.sleep(3)
			WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div[4]/iframe")))
			WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.message-component.message-button.no-children.focusable.sp_choice_type_11.last-focusable-el"))).click();
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("Failed to accept cookies.")
		#navigate to refine search options
		try:
			more = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CLASS_NAME,"atds-hero__more-options")))
			more.click();
			#postcode
			get_rand_post = ranDom.random_postCode()
			postcode = driver.find_element(by=By.ID, value="postcode")
			postcode.click();
			postcode.send_keys(get_rand_post)
		except TimeoutException as e:
			logging.error(e, exc_info=True)
			#await message.channel.send("Failed to go to `more search options`")
		#basically an if statement trying to wait and switch to the iframe and
		#accept cookies IF it comes up
		try: 
			WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div[4]/iframe")))
			WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.message-component.message-button.no-children.focusable.sp_choice_type_11.last-focusable-el"))).click();
			await asyncio.sleep(5)
		except Exception as e:
			logging.error(e, exc_info=True)
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
			driver.execute_script("window.scrollTo(0, 400)");
			WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//select[@id='minYear']"))).click();
			driver.find_element(By.XPATH,"//select[@id='minYear']/option[@value='2007']").click();
			await asyncio.sleep(1)
			driver.execute_script("window.scrollTo(0, 2000)");
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
		while i < pageCount:
			html = driver.page_source
			soup = BeautifulSoup(html, 'html.parser')

			with open(r'C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\urls.txt', 'r') as file:
				existing_urls = file.readlines()

			with open(r'C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\urls.txt', 'a') as file:
				for article in soup.find_all('article', class_='product-card js-standout-listing'):
					a_tag = article.find('a', class_='js-click-handler listing-fpa-link tracking-standard-link')
					if a_tag:
						url = a_tag['href']
						if 'http://autotrader.co.uk' + url + '\n' not in existing_urls:
							file.write('http://autotrader.co.uk' + url + '\n')

			try:
				next_page_button = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a[class='paginationMini--right__active'] i[class='icon']")))
				if next_page_button:
					next_page_button.click()
					i = i+1
					await asyncio.sleep(2)
			except TimeoutException as e:
				logging.error(e, exc_info=True)
				i = i+1
				#await message.channel.send("Couldn't get next page of listings")
		driver.quit()

#------- Listing handler end -------#

async def start():
	await getListings()
	await asyncio.sleep(2)
	global auto_trader_url
	with open(r'C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\urls.txt', 'r') as file:
		url_pool = file.readlines()
	for url in url_pool:
		auto_trader_url = url
		await asyncio.sleep(1)
		try:
			driver.get(url)
			try: #cookies
			 	WebDriverWait(driver, 3).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div[4]/iframe")))
			 	WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/div[2]/div[3]/div[2]/button[2]"))).click();
			except TimeoutException as e: #end cookies
				logging.error(e, exc_info=True)
			try: #get price_text
				global listing_price
				find_price = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html[1]/body[1]/div[2]/main[1]/div[1]/div[2]/aside[1]/section[1]/div[1]/div[1]/h2[1]")))
				listing_price = find_price.text
			except InvalidArgumentException as e: #end get price
				logging.error(e, exc_info=True)

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
			except TimeoutException as e:
				logging.error(e,exc_info=True)
			if not finance_option:
				driver.quit()
			else:
				await finance_handler()
				await asyncio.sleep(2)
				await getHPI(leads_channel)

		except TimeoutException as e:
			logging.error(e,exc_info=True)

async def run_schedule():
	schedule.every().day.at("15:10").do(lambda: asyncio.create_task(start()))
	while True:
	    schedule.run_pending()
	    await asyncio.sleep(1)

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
	asyncio.create_task(run_schedule())

if __name__ == '__main__':
    clientID = 'MTA2ODgzODc4OTM3MzUwOTY3Mg.GFApDS.0zYDIu4XqbBVsLrhwyK3WB2wok0gAVjA-Su85w'
    client.run(clientID)