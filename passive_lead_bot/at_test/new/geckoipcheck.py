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



proxyManager = ProxyManager()


gecko_path = os.path.join(os.environ['SystemRoot'], 'geckodriver.exe')
binary_path = os.path.normpath(os.path.join(os.environ['ProgramFiles'], 'Mozilla Firefox', 'firefox.exe'))
firefox_service = FirefoxService(executable_path = gecko_path)
binary_location = binary_path
proxy = proxyManager.get_random_proxy()
driver_options = webdriver.FirefoxOptions()
driver_options.set_preference('network.proxy.type', 1)
driver_options.add_argument("--proxy-server=http://"+proxy)
driver_options.add_argument("--user-agent="+proxyManager.get_random_UA())
driver = webdriver.Firefox(options=driver_options, firefox_binary=binary_location, service=firefox_service)

driver.get('https://www.whatismybrowser.com/')
user_agent = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//div[@class="string-major"]')))
ip_address = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//div[@class="string-minor"]')))
print(f"{user_agent.text} {ip_address.text}")
