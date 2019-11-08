# -*- coding: utf-8 -*-
import scrapy
from vacancyparser.items import VacancyparserItem


def compensation_min_max(compensation):
    c = str(compensation).replace("\xa0", " ").replace('—', '-')
    if c[:2] == "По":
        minimum = "По договорённости"
        maximum = "По договорённости"
    elif c[:2] == "от":
        minimum = int(''.join(filter(lambda x: x.isdigit(), c[3:])))
        maximum = "По договорённости"
    elif c[:2] == "до":
        minimum = "По договорённости"
        maximum = int(''.join(filter(lambda x: x.isdigit(), c[3:])))
    elif "-" in c:
        mi, ma = c.split("-")
        minimum = int(''.join(filter(lambda x: x.isdigit(), mi)))
        maximum = int(''.join(filter(lambda x: x.isdigit(), ma)))
    else:
        minimum = int(''.join(filter(lambda x: x.isdigit(), c)))
        maximum = int(''.join(filter(lambda x: x.isdigit(), c)))

    return minimum, maximum

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vakansii/kouch.html']

    def parse(self, response):
        next_page = response.css('a[class="icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-dalshe"]::attr(href)')\
            .extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacancy_link = response.css('div[class="_3syPg _3P0J7 _9_FPy"] a._3dPok::attr(href)').extract()
        for link in vacancy_link:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response):
        name = response.css('div._3MVeX h1[class="_3mfro rFbjy s1nFK _2JVkc"]::text').extract_first()
        salary = response.css('div._3MVeX span[class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]').extract_first()
        salary = salary.replace('<span class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc">', '').replace('<span>', '')\
            .replace('</span>', '').replace('<!-- -->', '')
        salary_min, salary_max = compensation_min_max(salary)
        salary_currency = salary.split('\xa0')[-1]
        vacancy_ref = response.url
        vacancy_source = response.css('div._29NVe div._2CsQi:last-child h4::text').extract_first()
        vacancy_city = response.css('span[class="_3mfro _1hP6a _2JVkc"]::text').extract_first()

        yield VacancyparserItem(name=name, vacancy_city=vacancy_city, salary_currency=salary_currency,
                                salary_max=salary_max, salary_min=salary_min, vacancy_ref=vacancy_ref,
                                vacancy_source=vacancy_source)
