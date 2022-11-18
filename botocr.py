#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Awesome Discord Bot."""

import argparse
import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv

import cogs
from utils.bot_logging import setup_logging
from utils.constants import IGNORE_COMMAND_NOT_FOUND

# Parse a .env file and then load all the variables found as environment variables.
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
deepltoken = os.getenv("DEEPL")
# Done

prefix = '!'

# --debug option
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="change prefix to '?'", action="store_true")
parser.add_argument("-v", "--verbosity", help="Verbosity", action="store_true")
args = parser.parse_args()
if args.debug:
    print("You are in debug mode.")
    print("Prefix is now '?'")
    prefix = '?'
# done with parsing options with argparser

# parameters for the bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, help_command=None,
                   description=None, case_insensitive=True, intents=intents)

cogs_list = [
    cogs.Ocr,
    ]


@bot.event
async def on_command_error(ctx, error):  # pylint: disable=unused-argument
    """Handle the CommandNotFound errors."""
    if isinstance(error, CommandNotFound):
        print(error)
        if error.args[0] in IGNORE_COMMAND_NOT_FOUND:
            logger.warning("Ignoring DCtrad commands : '%s'", error)
            return
    logger.warning("Ignoring : '%s'", error)


@bot.event
async def on_ready():
    """Log in Discord."""
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    bot.deepltoken = deepltoken
    print('------')
    bot.prefix = prefix
    for cog in cogs_list:
        await bot.add_cog(cog(bot))
    await bot.tree.sync()


setup_logging(Path(__file__).resolve().parent / 'logging.json')
logger = logging.getLogger(__name__)

if args.verbosity:
    print("Verbose mode, setLevel to DEBUG")
    logging.getLogger("cogs").setLevel(logging.DEBUG)

# logger.info("This is an INFO message on the root logger.")
# logger.warning("This is a WARNING message of the root logger")
# logger.error("This is a ERROR message of the root logger")
# logger.critical("This is a CRITICAL message of the root logger")

try:
    logger.info("New bot ran with discord.py version : %s", discord.__version__)
    bot.run(token)
except Exception:  # pylint: disable=broad-except
    logger.critical("bot crashed with discord.py version : %s", {discord.__version__})
    logger.critical("Unexpected critical error", exc_info=True)
