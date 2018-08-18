#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
bot_app.py

Main module for Discord palico-bot

"""

import asyncio
import json

import discord
import requests
from discord.ext import commands

Client = discord.Client()
bot = commands.Bot(command_prefix="!",
                   description="Monster Hunter World database bot")


@bot.event
async def on_ready():
    get_database()
    print("Bot ready!")
    bot.say("Hi!")


@bot.command(pass_context=True)
async def pepperoni(ctx):
    user = ctx.message.author
    await bot.say("Rip in pepperoni {}".format(user.mention))


def get_database():
    pass


def load_config():
    with open("palico-bot/config/config.json", "r") as config_file:
        return json.load(config_file)


if __name__ == "__main__":
    config = load_config()
    bot.run(config["bot_token"])
