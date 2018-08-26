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
prefix = "!"
bot = commands.Bot(command_prefix=prefix,
                   description="Monster Hunter World database bot")


equipment = {"gs": "great-sword",
             "ls": "long-sword",
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
             "waist": "waist",
             "head": "head",
             "chest": "chest",
             "legs": "legs",
             "gloves":"gloves"}

ranks = {"lr": "low",
         "hr": "high",
         "low-rank": "low",
         "high-rank": "high"}


def is_rank(value: str):
    """
    Checks whether the input is a rank or not.

    Args:
        value (str): A value to be checked.

    Returns:
        Boolean value indicating whether the given value is a rank or not.

    """

    return value in ranks or ranks.get(value) is not None


def is_equipment(value):
    """
        Checks whether the input is a rank or not.

    Args:
        value (str): A value to be checked.

    Returns:
        Boolean value indicating whether the given value is a rank or not.

    """

    return value in equipment or equipment.get(value) is not None


@bot.event
async def on_ready():
    print("Bot up & ready!")


@bot.command(pass_context=True)
async def get(ctx):
    """
    Tries to fetch the queried item(s) from the database.
    Input format:
        args[0]: item or set name
        args[1]: equipment
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
        await bot.say("You need to give the type of the item / set and the item type")
        return

    rank = None
    skip_args = 1
    # If the last argument is a rank
    if len_args > 2 and is_rank(args[-1]):
        rank = ranks[args[-1].lower()]
        skip_args = 2

    thing_type = args[0 - skip_args].lower()
    if not is_equipment(thing_type):
        await bot.say(
            "\"{}\" is not a set nor equipment type. Check {}help for info."
            .format(thing_type, prefix))
        return
    else:
        thing_type = equipment.get(thing_type) if thing_type in equipment else thing_type

    thing = " ".join(args[:-skip_args]).lower()
    print(thing, thing_type, rank)

    # Get the actual rank parameter
    if rank:
        rank = ranks[rank] if rank in ranks else rank

    dh = DataHandler.get_handler()
    await dh.get_thing(thing, thing_type, rank)


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
