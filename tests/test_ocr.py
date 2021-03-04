#!/usr/bin/env python

"""Tests Google vision OCR."""
from dotenv import load_dotenv
from cogs.ocr import detect_document


load_dotenv()


def test_ocr_page():
    url = "https://cdn.discordapp.com/attachments/778536711885815839/817034605512359990/King_In_Black_-_Black_Panther_2021_001-002.jpg"  # noqa: E501
    page = detect_document(url)
    expected = ('"Attend me, t\'challa.\n'
                'Take heed of what i say."\n'
                'Ororo...\n'
                'Nyc then "Every problem you may face, every obstacle in your way, is susceptible to proper planning."\n'
                '»4 don\'t think about her now.\n'
                '"Plan, my son. Plan well, with a sober mind. With an icy eye,')
    assert page == expected
