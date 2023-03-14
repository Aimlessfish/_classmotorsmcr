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
info_statement = "[INFO    ]"
proxy = proxyManager.get_random_proxy()
driver_options = webdriver.FirefoxOptions()
driver_options.add_argument("--proxy-server=http://"+proxy)
driver_options.add_argument("--user-agent="+proxyManager.get_random_UA())
driver = webdriver.Firefox(options=driver_options, firefox_binary=binary_location, service=firefox_service)

driver.get('https://www.whatismybrowser.com/')
user_agent = driver.find_element_by_xpath('//div[@class="string-major"]')
ip_address = driver.find_element_by_xpath('//div[@class="string-minor"]')
