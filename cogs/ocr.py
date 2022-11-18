#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Miscs cog."""

import logging

import deepl
import discord
from discord.ext import commands

from .utils import detect_document, no_ext

logger = logging.getLogger(__name__)


class Ocr(commands.Cog):
    """Cog for making OCR with a discord command."""
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def ocr(self, ctx, attachment: discord.Attachment):
        """Get text from image.

        Args:
            attachment (discord.Attachment): L'image à analyser
        """
        # attachment = ctx.message.attachments[0]
        image_url = attachment.url
        trad_name = no_ext(image_url.split("/")[-1]).replace("SPOILER_", "")
        async with ctx.channel.typing():
            extracted_text = detect_document(image_url)
        if len(extracted_text) > 2048:
            # Send result in a file
            file_ = f'trads/{trad_name}.txt'
            with open(file_, 'w', encoding='utf-8') as text:
                text.write(extracted_text)
            # await ctx.send(extracted_text[:100])
            file_to_send = discord.File(file_)
            await ctx.send(file=file_to_send)
        else:
            # send an embed
            embed = discord.Embed(title=trad_name,
                                  description=extracted_text)
            await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def octrad(self, ctx, attachment: discord.Attachment):
        """Get text from image.

        Args:
            attachment (discord.Attachment): L'image à analyser
        """
        # attachment = ctx.message.attachments[0]
        image_url = attachment.url
        trad_name = no_ext(image_url.split("/")[-1]).replace("SPOILER_", "")
        async with ctx.channel.typing():
            extracted_text = detect_document(image_url)
        print(extracted_text[:50])

        translator = deepl.Translator(self.bot.deepltoken)
        result = translator.translate_text(extracted_text, target_lang="FR")
        translated_text = result.text
        print("--------------------------")
        print(translated_text[:50])

        if len(extracted_text) > 2048:
            # Send result in a file
            file_ = f'trads/{trad_name}.txt'
            with open(file_, 'w', encoding='utf-8') as text:
                text.write(translated_text)
            # await ctx.send(extracted_text[:100])
            file_to_send = discord.File(file_)
            await ctx.send(file=file_to_send)
        else:
            # send an embed
            embed = discord.Embed(title=trad_name,
                                  description=translated_text)
            await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def ping(self, ctx):
        "Ping the bot."
        logger.info("Info message in cogs.ocr")
        logger.debug("Debug message in cogs.ocr")
        await ctx.send("Pong !")
