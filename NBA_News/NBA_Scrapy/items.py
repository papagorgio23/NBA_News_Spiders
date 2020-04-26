# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from datetime import datetime
from w3lib.html import remove_tags


def convert_date(text):
    # convert string like Mar 14, 2020 to Python date
    actual_date = text[-12:]
    actual_date = datetime.strptime(actual_date, '%b %d, %Y')
    return actual_date


def clean_articles(text):
    # clean up the articles
    article = text.split("Copyright")[0]
    article = article.replace("\n", " ")
    article = article.replace("Search Toggle Search Input ", "")
    article = article.strip()
    return article


class NBANewsItem(Item):
    # Fields to be scraped
    team = Field()
    url = Field()
    tags = Field()
    title = Field()
    date = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
        )
    article = Field(
        input_processor=MapCompose(remove_tags, clean_articles),
        output_processor=Join()
    )
