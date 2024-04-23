#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Miscs cog."""

import logging

# import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class Mod(commands.Cog):
    """Cog moderation purpose."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role("Modérateurs", "modo")
    async def cl(self, ctx, nbr_msg: int):
        """Clear n messages."""
        logger.info("clear messages was invoked")
        messages = [message async for message in ctx.channel.history(limit=nbr_msg + 1)]
        await ctx.channel.delete_messages(messages)

    @cl.error
    async def cl_error(self, ctx, error):
        """Handle error in !clear command (MissingAnyRole)."""
        logger.error(error)
