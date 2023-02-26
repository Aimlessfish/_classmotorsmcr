import discord
import asyncio
from reg_function import reg
import logging
import schedule
import time
import datetime
import os 

os.system("title !reg listener")

info_statement = "[INFO    ]"
now = datetime.datetime.now()
timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(intents=intents)
general_ID = '1068572399177584702'

logging.basicConfig(filename='errors.log', level=logging.ERROR)

print(f"[{timestamp}] {info_statement} [bot]: Loading...")

@client.event
# async def on_message(message):
    # if message.content.startswith('!reg'):
    #     args = message.content.split()[1:]
    #     arguments = "".join(args)
    #     with open('reg.txt', 'w') as f:
    #         f.write(arguments)
    #     await reg(message, *args)
async def on_message(message):
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    if message.author == client.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        if message.content.startswith('!reg'):
            args = message.content.split()[1:3]
            registration, miles = args
            now = datetime.datetime.now()
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
            print(f"{timestamp} {info_statement} [Console]: !reg command recieved for reg: {registration} with milage: {miles}")
            await message.channel.send("Please wait while i get the values..")
            await message.channel.send("If I do not reply after 3 minuntes please retry.")
            with open('reg.txt', 'w') as f:
                f.write(arguments)
            await reg(message, registration, miles)


@client.event
async def on_ready():
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {info_statement} Logged in as [{client.user}]')
    await client.wait_until_ready()
    guilds = client.guilds
    print(f'[{timestamp}] {info_statement} Connected to {len(guilds)} guild(s):')
    for guild in guilds:
        print(f'[{timestamp}] {info_statement} - {guild.name} (ID: {guild.id})')
        for channel in guild.channels:
            if channel.name == 'reg':
                print(f'[{timestamp}] {info_statement} - Found reg-channel in {guild.name} (ID: {guild.id}), channel ID: {channel.id}')
                reg_channel_id = client.get_channel(channel.id)


async def run_bot():
    try:
        await client.start("MTA3Njg4NTUzMjc5NTIxMTkzOA.GOvtxR.62XbZu2Zxzs7hI6HkHPydLU3zBkCSPZQHM3qvY")
        #await client.close()
    except Exception as e:
        logging.error(e, exc_info=True)

asyncio.run(run_bot())

