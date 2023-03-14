import os
import time
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
rawproxy = proxyManager.get_random_proxy()
proxy, port = rawproxy.split(':')
driver_options = webdriver.FirefoxOptions()
driver_options.set_preference('network.proxy.type', 1)
driver_options.set_preference("network.proxy.http", proxy)
driver_options.set_preference("network.proxy.http_port", int(port))
driver_options.set_preference("--user-agent="+proxyManager.get_random_UA())
driver = webdriver.Firefox(options=driver_options, firefox_binary=binary_location, service=firefox_service)

driver.get('https://www.whatismybrowser.com/')
time.sleep(10)

