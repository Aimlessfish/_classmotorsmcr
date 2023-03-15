from classManager import *
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

proxy_manager = ProxyManager()
proxy = proxy_manager.get_random_proxy()

driver = FirefoxDriver(proxy=proxy).get_driver()
driver.get("https://whatsmyip.com")
time.sleep(5)
raw_ipv4 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="shownIpv4"]')))
ipv4 = raw_ipv4.text
print(ipv4)