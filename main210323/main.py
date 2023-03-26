import time
import discord
import requests
import re 
import logging
import random
import asyncio
import schedule
import datetime
from classManager import ProxyManager
from classManager import FirefoxDriver
from classManager import ChromeDriver
from classManager import RandomManager
from classManager import FileManager
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

#-----------discord settings
intents = discord.Intents.default()
client = discord.Client(intents=intents)
#-----------discord settings

#-----------global settings
info_statement = "[INFO    ]"
logging.basicConfig(filename='lead_bot_errors.log', level=logging.ERROR)
proxyManager = ProxyManager()
fileManager = FileManager()
max_retry = 5
global activeDriver
#-----------global settings

			
