# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient


def compensation_min_max(compensation):
    c = str(compensation).replace("\xa0", " ")
    if c[:2] == "По":
        minimum = "По договорённости"
        maximum = "По договорённости"
    elif c[:2] == "от":
        minimum = int(''.join(filter(lambda x: x.isdigit(), c[3:])))
        maximum = "По договорённости"
    elif c[:2] == "до":
        minimum = "По договорённости"
        maximum = int(''.join(filter(lambda x: x.isdigit(), c[3:])))
    elif "—" in c:
        mi, ma = c.split("—")
        minimum = int(''.join(filter(lambda x: x.isdigit(), mi)))
        maximum = int(''.join(filter(lambda x: x.isdigit(), ma)))
    else:
        minimum = int(''.join(filter(lambda x: x.isdigit(), c)))
        maximum = int(''.join(filter(lambda x: x.isdigit(), c)))

    return minimum, maximum


class VacancyparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.scrapy_vacancy

    def process_item(self, item, spider):
        item['vacancy_source'] = spider.name
        if spider.name == 'sjru':
            compensation = item['salary_min']
            item['salary_min'], item['salary_max'] = compensation_min_max(compensation)
            if compensation != 'По договорённости':
                item['salary_currency'] = compensation.split('\xa0')[-1]

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item
