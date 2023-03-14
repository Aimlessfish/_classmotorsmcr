import time
import discord
import requests
import re 
import logging
import random
import asyncio
import schedule
import datetime
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

#-----------discord settings
intents = discord.Intents.default()
client = discord.Client(intents=intents)
#-----------discord settings

#-----------global settings
gecko_path = os.path.join(os.environ['SystemRoot'], 'geckodriver.exe')
binary_path = os.path.normpath(os.path.join(os.environ['ProgramFiles'], 'Mozilla Firefox', 'firefox.exe'))
firefox_service = FirefoxService(executable_path = gecko_path)
binary_location = binary_path
driver_options = webdriver.FirefoxOptions()
info_statement = "[INFO    ]"
logging.basicConfig(filename='lead_bot_errors.log', level=logging.ERROR)
#-----------global settings

max_retry = 5

# #-----init class as object
# randomManager = RandomManager()
# proxyManager = ProxyManager()
# fileManager = FileManager()
# #-------------------------
# proxy = proxyManager.get_random_proxy()
# driver_options.add_argument("--proxy-server=http://"+proxy)
# driver_options.add_argument("--user-agent="+proxyManager.get_random_UA())
driver_options.add_argument("-purgecaches")
driver_options.add_argument("-private-window")
driver = webdriver.Firefox(options=driver_options, firefox_binary=binary_location, service=firefox_service)
# driver = webdriver.Firefox(options=driver_options, executable_path = firefox_service)
driver.get("https://google.com")
driver.quit()