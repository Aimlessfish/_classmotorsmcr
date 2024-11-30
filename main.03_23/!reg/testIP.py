from classManager import FirefoxDriver
from classManager import ChromeDriver
from classManager import ProxyManager
import random
import requests
import time

proxyManager = ProxyManager()

drivers = [ChromeDriver, FirefoxDriver]
selected_driver = random.choice(drivers)
useragent = proxyManager.get_random_UA()
randomProxy = proxyManager.get_random_proxy()
proxy = proxyManager.testProxy(randomProxy)
while not proxy:
    proxyManager.remove_proxy(randomProxy)
    randomProxy = proxyManager.get_random_proxy()
    proxy = proxyManager.testProxy(randomProxy)

driverInstance = selected_driver.create(proxy, useragent)
driver_info = f"[SELECTED DRIVER    {driverInstance}]"
activeDriver = driverInstance.get_driver()

activeDriver.get("http://httpbin.org/ip")
time.sleep(10)