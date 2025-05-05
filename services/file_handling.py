import asyncio
import os
import sys
import time

from services.logger import logger

BOOK_PATH = "books/Муму.txt"
PAGE_SIZE = 1050

book: dict[int, str] = {}

def _get_part_text(text:str, start: int, size: int) -> tuple[str, int]:
    dividing_signs = ["?", ".", ",", "!", ":", ";"]
    end:int = min(size+start, len(text))
    while end < len(text) and text[end-1] in dividing_signs and text[end] in dividing_signs:
        end -= 1
    new_text: str = text[start:end]
    length: int = len(new_text)
    while length > 0:
        if new_text[length-1] in dividing_signs:
            break
        length -= 1
    return (new_text[:length], length)

def prepare_book(path: str) -> None:
    with open(path, "r", encoding="windows-1251") as file_content:
        text = file_content.read()
        text.strip()
        number_page = 0
        len_sum = 0
        while text != "":
            number_page += 1
            page, length = _get_part_text(text, 0, PAGE_SIZE)
            book[number_page] = page.lstrip()
            text = text[length:]
            if length == 0:
                logger.info(f"Оставшаяся часть: {text}")
    logger.info(f"Книга разделена на страницы:\n{len(book)}")

prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))