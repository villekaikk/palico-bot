#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
bot_app.py

Main module for Discord palico-bot

"""

import asyncio
import json
import os

import discord
from discord.ext import commands

from DataHandler import DataHandler

Client = discord.Client()
bot = commands.Bot(command_prefix="!",
                   description="Monster Hunter World database bot")

abbrevations = {"gs": "greatsword",
                "ls": "longsword",
                "gl": "gunlance",
                "hbg": "heavy-bowgun",
                "lbg": "light-bowgun",
                "l": "lance",
                "sns": "sword-and-shield",
                "cb": "charge-blade",
                "b": "bow",
                "ig": "insect-glaive",
                "h": "hammer",
                "db": "dual-blades",
                "hh": "hunting-horn",
                "sa": "switch-axe",
                "set": "set",
                "low-rank": "lr",
                "high-rank": "hr"}


@bot.event
async def on_ready():
    print("Bot up & ready!")


@bot.command(pass_context=True)
async def get(ctx):
    """
    Tries to fetch the queried item(s) from the database.
    Input format:
        args[1]: item or set name
        args[2]: item type or "set"
        args[3]: lr / hr (optional)

    Args:
        ctx (discord.Context): Discord Context object.
    
    Returns:
        String / JSON containing the query results. If the query found any
        hits, the results will be formatted for easier reading.

    """
    
    args = ctx.message.content.split(" ")[1:]  # Don't get the !get
    await bot.say("Args given: {}".format(args))
    print("this should still run")


@bot.command(pass_context=True)
async def pepperoni(ctx):
    user = ctx.message.author
    await bot.say("Rip in pepperoni {}".format(user.mention))


def load_config():
    """
    Loads the configuration file from pre-determined path.

    Returns:
        Config file in a JSON format.

    """

    with open("palico-bot/config/config.json", "r") as config_file:
        return json.load(config_file)


def init_dirs(config):
    """
    Initializes the file structure for the bot.

    Args:
        config (dict): Loaded in configuration file in JSON format.

    Returns:
        Nothing

    """

    res_path = os.path.join(config.get("resource_path", None))
    if not os.path.exists(res_path):
        os.makedirs(res_path)

    return


def init_palico():
    """
    Initializes all the functionalities of the bot.

    Returns:
        Nothing

    """

    config = load_config()
    init_dirs(config)

    dh = DataHandler(config["resource_path"])
    dh.prepare_data()

    bot.run(config.get("bot_token", None))

if __name__ == "__main__":
    init_palico()
