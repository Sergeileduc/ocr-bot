#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Miscs cog."""

import logging
import os
import re

import discord
from discord.ext import commands
from google.cloud import vision


logger = logging.getLogger(__name__)

LINE_BREAKS_PATTERN = r"([\w\s,])(?:\n)"
FIRST_WORD = re.compile(r'((?<=[\.\?!]\s)(\w+)|(?<=\")(\w+)|(^\w+))', flags=re.MULTILINE)  # noqa: E501


def no_ext(filename):
    return os.path.splitext(filename)[0]


def remove_dummy_line_breaks(longstring):
    # rstrip because last line break becomes
    return re.sub(LINE_BREAKS_PATTERN, r"\1 ", longstring).rstrip()


def remove_multiple_spaces(longstring):
    return re.sub(r" +", " ", longstring, flags=re.MULTILINE)


def cap(match):
    return(match.group().capitalize())


# def sentence_case(text):
#     # Split into sentences. Therefore, find all text that ends
#     # with punctuation followed by white space or end of string.
#     sentences = re.findall(r'[^.!?]+[.!?](?:\s|\Z)', text)

#     # Capitalize the first letter of each sentence
#     sentences = [x[0].upper() + x[1:] for x in sentences]

#     # Combine sentences
#     return ''.join(sentences)


def sentence_case(text):
    return FIRST_WORD.sub(cap, text)


def detect_document(uri):
    """Detect document features in an image."""
    # home = str(Path.home())

    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.document_text_detection(image=image)  # pylint: disable=no-member  # noqa: E501
    texts = response.text_annotations

    if texts:
        page = texts[0].description.lower()

        # Remove dummy line breaks
        page = remove_dummy_line_breaks(page)
        logger.debug("DUMMY LINE BREAKS :\n%s", page)

        # Remove double sapces
        page = remove_multiple_spaces(page)
        logger.debug("DOUBLE SPACES :\n%s", page)

        # Capitalize sentences
        page = sentence_case(page)
        logger.debug("SENTENCE CASES :\n%s", page)

        return page


class Ocr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ocr(self, ctx):
        """Get text from image."""
        attachment = ctx.message.attachments[0]
        image_url = attachment.url
        trad_name = no_ext(image_url.split("/")[-1]).replace("SPOILER_", "")
        async with ctx.channel.typing():
            extracted_text = detect_document(image_url)
        if len(extracted_text) > 2048:
            # Send result in a file
            file_ = f'trads/{trad_name}.txt'
            with open(file_, 'w') as text:
                text.write(extracted_text)
            # await ctx.send(extracted_text[:100])
            file_to_send = discord.File(file_)
            await ctx.send(file=file_to_send)
        else:
            # send an embed
            embed = discord.Embed(title=trad_name,
                                  description=extracted_text)
            await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        logger.info("Info message in cogs.ocr")
        logger.debug("Debug message in cogs.ocr")
        await ctx.send("Pong !")
