import discord
import asyncio
from main import reg
from main import reg_nomiles
import logging
import schedule
import time
import datetime
import os
from classManager import FirefoxDriver
from classManager import ChromeDriver
from classManager import ProxyManager
import random
import requests

os.system("title !reg listener")


def current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


info = f"[INFO    {current_time()}]"

intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(intents=intents)

logging.basicConfig(filename='discord_errors.log', level=logging.ERROR)

print(f"[{info}] [bot]: Loading...")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    proxyManager = ProxyManager()

    await message.channel.send("Proxy Selection Started.")
    drivers = [ChromeDriver, FirefoxDriver]
    selected_driver = random.choice(drivers)
    useragent = proxyManager.get_random_UA()
    randomProxy = proxyManager.get_random_proxy()
    proxy = proxyManager.testProxy(randomProxy)
    while not proxy:
        proxyManager.remove_proxy(randomProxy)
        randomProxy = proxyManager.get_random_proxy()
        proxy = proxyManager.testProxy(randomProxy)
    await message.channel.send("Proxy Selection Completed!")
    driverInstance = selected_driver.create(
        proxy=randomProxy, useragent=useragent)
    driver_info = f"[SELECTED DRIVER    {driverInstance}]"
    print(f"{info} {driver_info}")
    try:
        if message.content.startswith('!reg'):
            try:
                args = message.content.split()[1]
                registration = args
                if message.content == 2:
                    kwarg = message.content.split()[2]
                    miles = kwarg
                    print(f"{info} [Console]: !reg command recieved for reg: {registration} {miles}")
                    await message.channel.send("Please wait while i get the values..")
                    await message.channel.send("If I do not reply after 2 minutes something is wrong.")
                    with open('reg.txt', 'w') as f:
                        f.write(registration, miles)
                    await reg(message, registration, miles, driverInstance)
                else:
                    print(f"{info} [Console]: !reg command recieved for reg: {registration}")
                    await message.channel.send("Please wait while i get the values..")
                    await message.channel.send("If I do not reply after 2 minutes something is wrong.")
                    with open('reg.txt', 'w') as f:
                        f.write(registration)
                    await reg_nomiles(message, registration, driverInstance)
            except Exception as e:
                logging.error(e, exc_info=True)
    except Exception as e:
        logging.error(e, exc_info=True)


@client.event
async def on_ready():
    print(f'{info} Logged in as [{client.user}]')
    await client.wait_until_ready()
    guilds = client.guilds
    print(f'{info} Connected to {len(guilds)} guild(s):')
    for guild in guilds:
        print(f'{info} - {guild.name} (ID: {guild.id})')
        for channel in guild.channels:
            if channel.name == 'reg':
                print(f'{info} - Found reg-channel in {guild.name} (ID: {guild.id}), channel ID: {channel.id}')
                reg_channel_id = client.get_channel(channel.id)
                # await reg_channel_id.send("I am ready to handle !reg reg")
                # await reg_channel_id.send("Please use `DIRECT MESSAGE`")


async def run_bot():
    try:
        await client.start("MTA3Njg4NTUzMjc5NTIxMTkzOA.GOvtxR.62XbZu2Zxzs7hI6HkHPydLU3zBkCSPZQHM3qvY")
        # await client.close()
    except Exception as e:
        logging.error(e, exc_info=True)

asyncio.run(run_bot())
