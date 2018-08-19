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
                "set": "set"}

ranks = {"lr": "low",
         "hr": "high",
         "low-rank": "low",
         "high-rank": "high"}


@bot.event
async def on_ready():
    print("Bot up & ready!")


@bot.command(pass_context=True)
async def get(ctx):
    """
    Tries to fetch the queried item(s) from the database.
    Input format:
        args[0]: item or set name
        args[1]: item type or "set"
        args[2]: lr / hr (optional)

    Args:
        ctx (discord.Context): Discord Context object.
    
    Returns:
        String / JSON containing the query results. If the query found any
        hits, the results will be formatted for easier reading.

    """

    args = ctx.message.content.split(" ")[1:]  # Don't get the !get
    len_args = len(args)

    if len_args < 2:
        bot.say("You need to give the name of the item / set and the item type")

    rank = None
    skip_args = 1
    if len_args > 2 and args[-1] in ranks:
        rank = ranks[args[-1].lower()]
        skip_args = 2

    thing_type = args[0 - skip_args].lower()
    if thing_type not in abbrevations and not abbrevations.get(thing_type):
        await bot.say("What is \"{}\"".format(thing_type))
        return
    else:
        thing_type = abbrevations.get(thing_type) if  thing_type in abbrevations else thing_type

    thing = " ".join(args[:-skip_args]).lower()
    print(thing, thing_type, rank)

    # Get the actual rank parameter
    if rank:
        rank = abbrevations[rank] if rank in abbrevations else rank

    dh = DataHandler.get_handler()
    await dh.get_thing(thing, thing_type, rank)


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

    dh = DataHandler(config["resource_path"], bot)
    dh.prepare_data()

    bot.run(config.get("bot_token", None))

if __name__ == "__main__":
    init_palico()
