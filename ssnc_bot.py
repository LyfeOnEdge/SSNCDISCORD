#A discord bot for AkdM's switch serial number checker found here: https://github.com/AkdM/ssncpy
from discord.ext.commands import Bot
import configparser
import serial_checker
import requests
import json
import sys
import os

TOKEN = "" #<- You'll need to generate a bot token
PREFIX = '$' #<- set this to your desired prefix

global serials
serials = {}

config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], "config.ini"))

try:
    serials_filename = config.get("SSNC", "SerialsJSON")
    with open(serials_filename) as f:
        serials = json.load(f)
except:
    serials_url = config.get("SSNC", "SerialsURL")
    req = requests.get(serials_url)
    if req.status_code == 200:
        serials = req.json()

client = Bot(command_prefix=PREFIX)

@client.command()
async def sn( sn):
    await client.say("{} - {}".format(sn, serial_checker.check(serials, sn)))

client.run(TOKEN)