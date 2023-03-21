import random
import os
from selenium import webdriver
from selenium.webdriver import Firefox, FirefoxOptions, Proxy
from selenium.webdriver.firefox.service import Service as FirefoxService

class FirefoxHandler:
    def __init__(self, headless=False, private_mode=True, disable_cache=True, block_cookies=True, proxy=None):
        self.gecko_path = os.path.join(os.environ['SystemRoot'], 'geckodriver.exe')
        self.binary_path = os.path.normpath(os.path.join(os.environ['ProgramFiles'], 'Mozilla Firefox', 'firefox.exe'))
        self.firefox_service = FirefoxService(executable_path=self.gecko_path)
        self.binary_location = self.binary_path
        self.options = FirefoxOptions()
        self.options.set_preference("browser.privatebrowsing.autostart", private_mode)
        self.options.set_preference("browser.cache.disk.enable", not disable_cache)
        self.options.set_preference("browser.cache.memory.enable", not disable_cache)
        self.options.set_preference("network.cookie.cookieBehavior", block_cookies)
        if proxy:
            self.options.proxy = Proxy({'proxyType': 'manual', 'httpProxy': proxy, 'sslProxy': proxy})

    def get_driver(self):
        return Firefox(options=self.options, firefox_binary=self.binary_location, service=self.firefox_service)

class ChromeHandler:
	def __init__(self):
		self.chromeOptions = webdriver.ChromeOptions()
		self.ChromeDriver = webdriver.Chrome(options = self.chromeOptions)

		def chromeOptions(self):
			return self.chromeOptions




chrome_handler = ChromeHandler()
chrome_options=chrome_handler.chromeOptions

firefox_handler = FirefoxHandler()
firefox = firefox_handler.get_driver()


chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--proxy-server=http://"+proxy)
chrome = chrome_handler.ChromeDriver
chrome.get("https://google.com")
firefox.get("https://google.com")