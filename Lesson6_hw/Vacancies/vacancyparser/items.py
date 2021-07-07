# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def name_modify(values):
    return values.replace('<h1 data-qa="vacancy-title" itemprop="title" class="header">', '')\
               .replace('<span class="highlighted">', '').replace('</span>', '').replace('</h1>', '')\
               .replace('<span>', '').replace('<h1 class="header" data-qa="vacancy-title" itemprop="title">', '')


def str_to_int(values):
    return int(values)


def salary_clean(values):
    return values.replace('<span class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc">', '').replace('<span>', '')\
        .replace('</span>', '').replace('<!-- -->', '')



class VacancyparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(input_processor=MapCompose(name_modify), output_processor=TakeFirst())
    salary_min = scrapy.Field(input_processor=MapCompose(str_to_int), output_processor=TakeFirst())
    salary_max = scrapy.Field(input_processor=MapCompose(str_to_int), output_processor=TakeFirst())
    salary_currency = scrapy.Field(output_processor=TakeFirst())
    vacancy_ref = scrapy.Field(output_processor=TakeFirst())
    vacancy_source = scrapy.Field()
    vacancy_city = scrapy.Field(output_processor=TakeFirst())


class VacancyparserItemSJ(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    salary_min = scrapy.Field(input_processor=MapCompose(salary_clean), output_processor=TakeFirst())
    salary_max = scrapy.Field()
    salary_currency = scrapy.Field()
    vacancy_ref = scrapy.Field(output_processor=TakeFirst())
    vacancy_source = scrapy.Field()
    vacancy_city = scrapy.Field(output_processor=TakeFirst())

