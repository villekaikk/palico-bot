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

import Weblib

Client = discord.Client()
bot = commands.Bot(command_prefix="!",
                   description="Monster Hunter World database bot")

weblib = Weblib.Weblib()

resources = ["armor", "weapons", "charms"]


@bot.event
async def on_ready():
    print("Bot ready!")


@bot.command(pass_context=True)
async def on_message(msg: discord.message):
    """
    Tries to fetch the queried item(s) from the database.

    Args:
        msg (Message): Discord message object.
    
    Returns:
        String / JSON containing the query results. If the query found any
        hits, the results will be formatted for easier reading.

    """
    pass


@bot.command(pass_context=True)
async def pepperoni(ctx):
    user = ctx.message.author
    await bot.say("Rip in pepperoni {}".format(user.mention))


def should_get_data(res_path: str):
    """
    Looks up if all the necessary resource files are already saved to the 
    directory.

    Args:
        res_path (str): Path to the resources folder.

    Returns:
        Boolean value indicating whether the data should be fetched or not

    """
    
    for r in resources:
        res = os.path.join(res_path, r)
        if not os.path.exists("{}.json".format(res)):
            return True
        print("No need to fetch {}".format(r))
    
    return False

def get_resource(resource: str):
    """
    Fetches the given resource and saves it to the "resources" directory.

    Args:
        resource (str): name of the resource to be getten.

    Returns:
        Nothing

    """

    res_json = weblib.get(resource)
    save_path = os.path.join("palico-bot", "resources", resource)

    with open("{}.json".format(save_path), "w") as res_file:
        json.dump(res_json, res_file, indent=4)


def get_database(config: dict):
    """
    Fetches the MHW database over REST API and saves it locally for easier
    access.

    Args:
        config (dict): Loaded in config file in JSON format.

    Returns:
        Nothing

    """

    if should_get_data(config.get("resource_path")):
        for r in resources:
            get_resource(r)

    return


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
    get_database(config)
    bot.run(config.get("bot_token", None))

if __name__ == "__main__":
    init_palico()
