# -*- coding: utf-8 -*-
import scrapy
from vacancyparser.items import VacancyparserItemSJ
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response):
        next_page = response.css('a[class="icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-dalshe"]::attr(href)')\
            .extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy_link = response.css('div[class="_3syPg _3P0J7 _9_FPy"] a._3dPok::attr(href)').extract()
        for link in vacancy_link:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=VacancyparserItemSJ(), response=response)
        loader.add_css('name', 'div._3MVeX h1[class="_3mfro rFbjy s1nFK _2JVkc"]::text')
        loader.add_css('salary_min', 'div._3MVeX span[class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]')
        ref = response.url
        loader.add_value('vacancy_ref', ref)
        loader.add_css('vacancy_city', 'span[class="_3mfro _1hP6a _2JVkc"]::text')
        # name = response.css('div._3MVeX h1[class="_3mfro rFbjy s1nFK _2JVkc"]::text').extract_first()
        # salary = response.css('div._3MVeX span[class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]').extract_first()
        # salary = salary.replace('<span class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc">', '').replace('<span>', '').replace('</span>', '').replace('<!-- -->', '')
        # salary_min, salary_max = compensation_min_max(salary)
        # salary_currency = salary.split('\xa0')[-1]
        # vacancy_ref = response.url
        # vacancy_source = response.css('div._29NVe div._2CsQi:last-child h4::text').extract_first()
        # vacancy_city = response.css('span[class="_3mfro _1hP6a _2JVkc"]::text').extract_first()

        yield loader.load_item()
