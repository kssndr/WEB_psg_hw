# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values


def param_modify(values):
    param = {}
    p = values.replace('<li class="item-params-list-item"> <span class="item-params-label">', '').replace('</span>', '')\
        .replace('</li>', '')
    name, value = p.split(": ")
    param[name] = value
    return param


class AvitoParserItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    parameters = scrapy.Field(input_processor=MapCompose(param_modify))
