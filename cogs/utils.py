#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Miscs cog."""

import logging
import os
import re

from google.cloud import vision

logger = logging.getLogger(__name__)

LINE_BREAKS_PATTERN = r"([\w\s,])(?:\n)"
FIRST_WORD = re.compile(r'((?<=[\.\?!]\s)(\w+)|(?<=\")(\w+)|(^\w+))', flags=re.MULTILINE)  # noqa: E501


def no_ext(filename):
    """Remove extension."""
    return os.path.splitext(filename)[0]


def remove_dummy_line_breaks(longstring):
    """Remove dummy line breaks"""
    # rstrip because last line break becomes
    return re.sub(LINE_BREAKS_PATTERN, r"\1 ", longstring).rstrip()


def remove_multiple_spaces(longstring):
    "Remove multiple spaces."
    return re.sub(r" +", " ", longstring, flags=re.MULTILINE)


def cap(match):
    "Capitalize sentence."
    return (match.group().capitalize())


# def sentence_case(text):
#     # Split into sentences. Therefore, find all text that ends
#     # with punctuation followed by white space or end of string.
#     sentences = re.findall(r'[^.!?]+[.!?](?:\s|\Z)', text)

#     # Capitalize the first letter of each sentence
#     sentences = [x[0].upper() + x[1:] for x in sentences]

#     # Combine sentences
#     return ''.join(sentences)


def sentence_case(text):
    """Transform text, with multiple sentences, by adding Capital Letters on the
    beginning of each sentence.

    Args:
        text (str): the text to transform

    Returns:
        str: Capitalized text
    """
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
    return None
