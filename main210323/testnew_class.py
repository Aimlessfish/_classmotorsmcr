from classManager import ProxyManager
from classManager import FirefoxDriver
from classManager import ChromeDriver
from classManager import RandomManager
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

proxy_manager = ProxyManager()
proxy = proxy_manager.get_random_proxy()
maxretry = 5
i = 0 
while i != maxretry:
	proxy = proxy_manager.get_random_proxy()
	fox_driver = FirefoxDriver(proxy=proxy).get_driver()
	fox_driver.get("https://whatsmyip.com")
	if "Whats My" in fox_driver.title:
		break
	else:
		proxy_manager.remove_proxy(proxy)
		fox_driver.quit()
		i +=1
raw_ipv4 = WebDriverWait(fox_driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/section/div/div/div/div[2]/p[1]')))
ipv4 = raw_ipv4.text
print(ipv4)
fox_driver.quit()
i =0
while i != 5:
	proxy = proxy_manager.get_random_proxy()
	makeChrome = ChromeDriver.create()
	chromeOptions = ChromeDriver.chromeOptions()
	chrome_driver = makeChrome.chromeDriver()
	chromeOptions.add_argument("--proxy-server="+proxy)
	chrome_driver.get("https://whatsmyip.com")
	if "Whats My" in chrome_driver.title:
		break
	else:
		proxy_manager.remove_proxy(proxy)
		chrome_driver.quit()
		i +=1
	raw_ipv4 = WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/section/div/div/div/div[2]/p[1]')))
	ipv4 = raw_ipv4.text
	print(ipv4)