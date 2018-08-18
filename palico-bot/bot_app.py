#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
bot_app.py

Main module for Discord palico-bot

"""

import discord
import json
import requests
import asyncio

from discord.ext.commands import Bot
from discord.ext import commands

config = load_config()
Client = discord.Client()
bot = Bot(command_prefix="#", description="Monster Hunter World database bot")

bot.run(config["bot_token"])

@bot.event
async def on_ready():
    get_database()
    print("Bot ready!")


@bot.command()
async def pepperoni(ctx):
    pass

def get_database():
    pass

def load_config():
    with open("config/config.json", "r") as config_file:
        return json.load(config_file)