#!/usr/bin/env python

"""Tests Google vision OCR."""
from dotenv import load_dotenv

from cogs.ocr import detect_document

load_dotenv()

# for preparing the tests
# ocr_text = open(Path("tests") / "ocr.txt", "w")


def test_ocr_page():
    """Test google ocr."""
    url = "https://cdn.discordapp.com/attachments/1043282081888878652/1306184004080373780/King_In_Black_-_Black_Panther_2021_001-002.jpg?ex=6735be26&is=67346ca6&hm=ed63e39046c9fc9cf31cd6022fc32b7de1372b89d294f6d1a7922579877a1074&"  # noqa: E501
    page = detect_document(url)
    expected = ('"Attend me, t\'challa.\n'
                'Take heed of what i say."\n'
                'Ororo...\n'
                '"Every problem you may face, every obstacle in your way, is susceptible to proper planning."\n'
                'Don\'t think about her now.\n'
                'Nyc.\n'
                'Then "Plan, my son. Plan well. With a sober mind. With an icy eye.')

    # For preparing the tests...
    # ocr_text.write(page + '\n')
    # ocr_text.write('------------------------------\n')

    assert page == expected
