#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Miscs cog."""

import logging
import os
import re

import discord
from discord.ext import commands
from google.cloud import vision, vision_v1


logger = logging.getLogger(__name__)

LINE_BREAKS_PATTERN = r"([\w\s,])(?:\n)"


def no_ext(filename):
    return os.path.splitext(filename)[0]


def remove_dummy_line_breaks(longstring):
    return re.sub(LINE_BREAKS_PATTERN, r"\1 ", longstring)


def remove_double_spaces(longstring):
    return longstring.replace("  ", " ")


def sentence_case(text):
    # Split into sentences. Therefore, find all text that ends
    # with punctuation followed by white space or end of string.
    sentences = re.findall(r'[^.!?]+[.!?](?:\s|\Z)', text)

    # Capitalize the first letter of each sentence
    sentences = [x[0].upper() + x[1:] for x in sentences]

    # Combine sentences
    return ''.join(sentences)


def detect_document(uri):
    """Detect document features in an image."""
    # home = str(Path.home())

    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.document_text_detection(image=image)  # pylint: disable=no-member  # noqa: E501

    breaks = vision_v1.types.TextAnnotation.DetectedBreak.BreakType
    paragraphs = []
    lines = []

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                para = ""
                line = ""
                for word in paragraph.words:
                    for symbol in word.symbols:
                        line += symbol.text
                        if symbol.property.detected_break.type_ == breaks.SPACE:
                            line += ' '
                        if symbol.property.detected_break.type_ == breaks.EOL_SURE_SPACE:  # noqa: E 501
                            line += ' '
                            lines.append(line)
                            para += line
                            line = ''
                        if symbol.property.detected_break.type_ == breaks.LINE_BREAK:  # noqa: E501
                            lines.append(line)
                            para += line
                            line = ''
                paragraphs.append(para)

    # Make a page string
    page = '\n'.join(paragraphs).lower()

    # Remove dummy line breaks
    page = remove_dummy_line_breaks(page)

    # Remove double sapces
    page = remove_double_spaces(page)

    # Capitalize sentences
    page = sentence_case(page)

    # page_num = no_ext(uri.split("/")[-1])

    # page = f"{page_num}\n" + page

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
            #Send result in a file
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
