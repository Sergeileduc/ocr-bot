#!/usr/bin/env python

"""Tests Google vision OCR."""
from dotenv import load_dotenv
from cogs.ocr import detect_document
from pathlib import Path


load_dotenv()

# for preparing the tests
# ocr_text = open(Path("tests") / "ocr.txt", "w")

def test_ocr_page():
    url = "https://cdn.discordapp.com/attachments/819981551353724949/1018078436184567808/King_In_Black_-_Black_Panther_2021_001-002.jpg"  # noqa: E501
    page = detect_document(url)
    expected = ('"Attend me, t\'challa.\n'
                'Take heed of what i say."\n'
                'Ororo...\n'
                '4.\n'
                '"Every problem you may face, every obstacle in your way, is susceptible to proper planning."\n'
                'Don\'t think about her now.\n'
                'Wallbed.diblokk nyc then.\n'
                'Tr faoli "Plan, my son. Plan well. With a sober mind. With an icy eye.')

    # For preparing the tests...
    # ocr_text.write(page + '\n')
    # ocr_text.write('------------------------------\n')

    assert page == expected
