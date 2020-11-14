#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Awesome Discord Bot."""

import argparse
import logging
import os
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

import cogs

from utils.bot_logging import setup_logging


# Parse a .env file and then load all the variables found as environment variables.
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
# Done

prefix = '!'

# --debug option
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug",
                    help="change prefix to '?'", action="store_true")
args = parser.parse_args()
if args.debug:
    print("You are in debug mode.")
    print("Prefix is now '?'")
    prefix = '?'
# done with parsing options with argparser

bot = commands.Bot(command_prefix=prefix, help_command=None,
                   description=None, case_insensitive=True)

cogs_list = [
    cogs.Ocr,
    ]


@bot.event
async def on_ready():
    """Log in Discord."""
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.prefix = prefix
    for cog in cogs_list:
        bot.add_cog(cog(bot))


setup_logging()
logger = logging.getLogger(__name__)

logger.info("This is an INFO message on the root logger.")
# logger.warning("This is a WARNING message of the root logger")
# logger.error("This is a ERROR message of the root logger")
# logger.critical("This is a CRITICAL message of the root logger")

try:
    logger.info(f"New bot ran with discord.py version : {discord.__version__}")
    bot.run(token)
except Exception:
    logger.critical(f"bot crashed with discord.py version : {discord.__version__}")
    logger.critical("Unexpected critical error", exc_info=True)
