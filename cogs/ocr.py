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
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
    async def ocr(self, ctx: commands.Context, attachment: discord.Attachment):
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
            await ctx.send(file=discord.File(file_))
        else:
            # send an embed
            embed = discord.Embed(title=trad_name,
                                  description=extracted_text)
            await ctx.send(embed=embed)

    @commands.hybrid_command(aliases=['octrad', 'ocrtrad'])
    async def trad(self, ctx: commands.Context, attachment: discord.Attachment):
        """Get text from image, and translate it.

        Args:
            attachment (discord.Attachment): L'image à analyser
        """
        # attachment = ctx.message.attachments[0]
        image_url = attachment.url
        trad_name = no_ext(image_url.split("/")[-1]).replace("SPOILER_", "")
        async with ctx.channel.typing():
            extracted_text = detect_document(image_url)
            translator = deepl.Translator(self.bot.deepltoken)
            result = translator.translate_text(extracted_text, target_lang="FR")
        translated_text = result.text

        if len(translated_text) > 2048:  # Send result in a file
            file_ = f'trads/{trad_name}.txt'
            with open(file_, 'w', encoding='utf-8') as text:
                text.write(translated_text)
            await ctx.send(file=discord.File(file_))
        else:  # send an embed
            embed = discord.Embed(title=trad_name, description=translated_text)
            await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def usage(self, ctx: commands.Context):
        """Get API usage.
        """
        translator = deepl.Translator(self.bot.deepltoken)
        usage = translator.get_usage()

        descr = (f"Vous avez utilisé {(count := int(usage.character.count)):,} sur {(limit := int(usage.character.limit)):,} mots.\n"
                 f"Votre ratio d'usage DeepLest de {count/limit:.2%}\n"
                 f"Votre API est {'valide' if usage.character.valid else 'invalide'}.\n"
                 f"{'Vous avez dépassé la limite' if usage.character.limit_reached else 'Limite pas encore dépassée.'}.")  # noqa: E501

        embed = discord.Embed(title="API usage",
                              description=descr)
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context):
        "Ping the bot."
        logger.info("Info message in cogs.ocr")
        logger.debug("Debug message in cogs.ocr")
        await ctx.send("Pong !")
