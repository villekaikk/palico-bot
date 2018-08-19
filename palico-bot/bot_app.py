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
                "lr": "low",
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

    thing = args[0]
    thing_type = args[1].lower()
    rank = args[2].lower() if len(args) > 2 else None

    # Get the actual rank parameter
    if rank:
        rank = abbrevations[rank] if rank in abbrevations else rank

    #print("Querying: {} {} with {}".format(thing, thing_type, rank))
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
