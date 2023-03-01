import time
import discord
import requests
import re 
import logging
import random
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
import asyncio
import schedule

driver_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options = driver_options)

async def geturl():
	driver.get("https://autotrader.co.uk")
	await asyncio.sleep(10)

asyncio.run(geturl())
