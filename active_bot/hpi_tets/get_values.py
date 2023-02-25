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

logging.basicConfig(filename='errors.log', level=logging.ERROR)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options = options)

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

def get_values():
	driver.get("https://hpivaluations.com/report/view/VA25409334-FJ19RSV")
	time.sleep(5)
	try:
		cookies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#onetrust-accept-btn-handler")))
		cookies.click();
	except TimeoutException as e:
		logging.error(e,exc_info=True)
	try:
		hpi_span1_low = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div/span[1]/span[1]")))
		hpi_span1_high = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div/span[3]/span[1]")))
		global hpi_span1_low_data
		global hpi_span1_high_data
		hpi_span1_low_data = hpi_span1_low.text.strip()
		hpi_span1_high_data = hpi_span1_high.text.strip()
	except Exception as e:
		logging.error(e,exc_info=True)

	try:
		navpoor = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/a[1]")))
		navpoor.click();
		try:
			time.sleep(2)
			hpi_span_low_poor = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div/span[1]/span[1]")))
			hpi_span_high_poor = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div/span[3]/span[1]")))
			global hpi_span2_low_data
			global hpi_span2_high_data
			hpi_span2_low_data = hpi_span_low_poor.text.strip()
			hpi_span2_high_data = hpi_span_high_poor.text.strip()
		except TimeoutException as e:
			logging.error(e,exc_info=True)
	except TimeoutException as e:
		logging.error(e,exc_info=True)

	try:
		navbest = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/a[3]")))
		navbest.click();
		try:
			time.sleep(2)
			hpi_span_low_best = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div/span[1]/span[1]")))
			hpi_span_high_best = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[1]/div/div/span[3]/span[1]")))
			global hpi_span3_low_data
			global hpi_span3_high_data
			hpi_span3_low_data = hpi_span_low_best.text.strip()
			hpi_span3_high_data = hpi_span_high_best.text.strip()
		except TimeoutException as e:
			logging.error(e,exc_info=True)
	except TimeoutException as e:
		logging.error(e,exc_info=True)
	try:
		navforeCourt = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[2]")))
		navforeCourt.click();
		try:
			global foreCourt_low_data
			global foreCourt_high_data
			foreCourt_low = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/span[1]/span[1]")))
			foreCourt_low_data = foreCourt_low.text.split()
			foreCourt_high = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/span[3]/span[1]")))
			foreCourt_high_data = foreCourt_high.text.split()
		except TimeoutException as e:
			logging.error(e,exc_info=True)
	except TimeoutException as e:
		logging.error(e,exc_info=True)
	try:
		navprivate = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/ul/li[1]")))
		navprivate.click();
		try:
			global private_low_data
			global private_high_data
			private_low = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/span[1]/span[1]")))
			private_high = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div/span[3]/span[1]")))
			private_low_data = private_low.text.split()
			private_high_data = private_high.text.split()
		except TimeoutException as e:
			logging.error(e,exc_info=True)
	except TimeoutException as e:
		logging.error(e,exc_info=True)
get_values()
print(f"trade_poor_low: ", hpi_span2_low_data," | ","trade_poor_high: ", hpi_span2_high_data,"\n",
	"trade_good_low: ", hpi_span1_low_data," | ","trade_good_high: ", hpi_span1_high_data,"\n",
	"trade_best_low: ", hpi_span3_low_data," | ","trade_best_high: ", hpi_span3_high_data,"\n",
	"foreCourt_low: ",foreCourt_low_data," | ","foreCourt_high: ", foreCourt_high_data,"\n",
	"private_low: ", private_low_data," | ", "private_high: ", private_high_data)
