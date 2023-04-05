import random
import os
from selenium import webdriver
from selenium.webdriver import Firefox, FirefoxOptions, Proxy
from selenium.webdriver.firefox.service import Service as FirefoxService


max_width = 2560
max_height = 1600
#-----------------------------Broswer Managers-----------------------------#
class FirefoxDriver:
    def __init__(self, headless=False, private_mode=True, disable_cache=True, block_cookies=True, proxy=None, useragent=None):
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
        if useragent:
            self.options.set_preference("general.useragent.override", useragent)

    def get_driver(self):
        return Firefox(options=self.options, firefox_binary=self.binary_location, service=self.firefox_service)

    @classmethod
    def create(cls):
        return cls()

class ChromeDriver:
	def __init__(self, proxy=None, useragent=None):
		self.capabilities = webdriver.DesiredCapabilities().CHROME
		self.capabilities['acceptInsecureCerts'] = True
		self.chromeOptions = webdriver.ChromeOptions()
		self.chromeOptions.add_argument("--start-maximized")
		if useragent:
			self.chromeOptions.add_argument("--user-agent="+useragent)
		if proxy:
			self.chromeOptions.add_argument("--proxy-server=http://"+proxy)
		self.ChromeDriver = webdriver.Chrome(options = self.chromeOptions)

	def loadSize(self):
		self.height=random.randint(800, 2560)
		self.width=random.randint(800,1920)
		return self.height, self.width
		
	def chromeOptions(self):
		return self.chromeOptions

	def get_driver(self):
		return self.ChromeDriver

	@classmethod
	def create(cls):
            return cls()
		
#---------------------------Broswer Managers END---------------------------#
class RandomManager:
	def __init__(self):
		self.namesfile = r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\names.txt"
		self.postcodefile = r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\postcode.txt"
		self.addressfile = r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\addresses.txt"
		self.names = []
		self.postcodes = []
		self.addresses = []
		self.load_names()
		self.load_postcodes()
		self.load_addresses()

	def load_names(self):
		with open(self.namesfile, "r") as f:
			self.names = [line.strip() for line in f]
			f.close()

	def load_postcodes(self):
		with open(self.postcodefile, "r") as f:
			self.postcodes = [line.strip() for line in f]
			f.close()

	def load_addresses(self):
		with open(self.addressfile, "r") as f:
			self.addresses = [line.strip() for line in f]
			f.close()

	def randSize(self):
		width = random.randint(200, max_width)
		height = random.randint(200, max_height)
		if width < 1020 or height < 1680:
		# Set the minimum screen size to 1020x1680
			width = 1020
			height = 1680
		return width, height

	def get_random_name(self):
		if not self.names:
			self.load_names()
		return random.choice(self.names)

	def get_random_postcode(self):
		if not self.postcodes:
			self.load_postcodes()
		return random.choice(self.postcodes)

	def get_random_address(self):
		ranAdd = random.choice(self.addresses).strip('"\n')
		street_town, postcode = ranAdd.rsplit(',',1)
		town = street_town.rsplit(',',1)[-1].strip()
		street = street_town.rsplit(',',1)[0].strip()
		houseNo = street.split()[0].strip()
		return houseNo, street, town, postcode

	def create_hpi_name(self):
		if not self.names:
			self.load_names()
		hpi_name = random.choice(self.names).strip()
		return hpi_name[:len(hpi_name)//2]+" "+hpi_name[len(hpi_name)//2]

	def random_phone(self):
		phone_suffix = str(random.randint(0,999999999)).zfill(9)
		phone_number= "07"+phone_suffix
		return phone_number

	def createEmail(self):
		ranEmail = self.get_random_name()+self.random_phone()+"@mynes.com"
		with open(r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\email.txt","w") as f:
			f.write(ranEmail)
			f.close()
		return ranEmail


class ProxyManager:
	def __init__(self):
		self.proxyfile = r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\proxy.txt"
		self.uafile = r"C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\user-agents.txt"
		self.useragents = []
		self.proxies = []
		self.load_proxies()
		self.load_UA()

	def load_proxies(self):
		with open(self.proxyfile, "r") as f:
			self.proxies = [line.strip() for line in f]

	def load_UA(self):
		with open(self.uafile, "r") as f:
			self.useragents = [line.strip() for line in f]

	def get_random_UA(self):
		if not self.useragents:
			self.load_UA()
		return random.choice(self.useragents)

	def get_random_proxy(self):
		if not self.proxies:
			self.load_proxies()
		return random.choice(self.proxies)

	def remove_proxy(self, proxy):
	    if proxy in self.proxies:
	        self.proxies.remove(proxy)
	        with open(self.proxyfile, "w") as f:
	            f.writelines(self.proxies)
	    else:
	        print(f"{proxy} not found in proxy list.")

class FileManager():
	def __init__(self):
		self.urlfile = r'C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\urls.txt'
		self.validfile = r'C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\valid_url.txt'
		self.emailfile = r'C:\Users\Administrator\Desktop\_classmotorsmcr-main\required_list\email.txt'
		self.urls = []
		self.validurls = []
		self.loadurl()
		self.loadvalid()
		self.loademail()

	def loadurl(self):
		with open(self.urlfile, "r") as f:
			self.urls = [line.strip() for line in f]
		return self.urls

	def loadvalid(self):
		with open(self.validfile, "r") as f:
			self.validurls = [line.strip() for line in f]
		return self.validurls

	def loademail(self):
		with open(self.emailfile, "r") as f:
			self.email = f.readlines()
		return self.email

	def write_url(self, url):
		with open(self.urlfile, "a") as f:
			f.write(url+"\n")

	def write_valid(self, valid_url):
		with open(self.validfile, "a") as f:
			f.write(valid_url+"\n")


