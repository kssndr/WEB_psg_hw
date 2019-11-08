# -*- coding: utf-8 -*-
import scrapy
from vacancyparser.items import VacancyparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=коуч&area=113&from=cluster_area&showClusters=true']

# Сбор данных со всех страниц (пока не вернется None)
    def parse(self, response):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

# Сбор из собранных данных только ссылки непосредственно на страницу вакансии
        vacancy_link = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)'
        ).extract()

# Заново собираем в response теперь данные непосредственно те которые нужны со страницы вакансии
        for link in vacancy_link:
            yield response.follow(link, self.vacancy_parse)

# Сама функция по сбору нужных данных со страницы вакансии
    def vacancy_parse(self, response):
        name_ = response.css('div.vacancy-title h1.header').extract_first()  # не полное название
        name = name_.replace('<h1 data-qa="vacancy-title" itemprop="title" class="header">', '').replace('<span class="highlighted">', '').replace('</span>', '').replace('</h1>', '').replace('<span>', '').replace('<h1 class="header" data-qa="vacancy-title" itemprop="title">', '')
        # salary_text = response.css('p.vacancy-salary::text').extract_first()
        salary_min = response.css('div.vacancy-title span[itemprop="baseSalary"] meta[itemprop="minValue"]::attr('
                                  'content)').extract_first()
        salary_max = response.css('div.vacancy-title span[itemprop="baseSalary"] meta[itemprop="maxValue"]::attr('
                                  'content)').extract_first()
        salary_max_do = response.css('div.vacancy-title span[itemprop="baseSalary"] meta[itemprop="Value"]::attr('
                                  'content)').extract_first()
        if salary_max_do:
            salary_max = salary_max_do
        else:
            salary_max = salary_max

        salary_currency = response.css('div.vacancy-title span[itemprop="baseSalary"] meta['
                                       'itemprop="currency"]::attr(content)').extract_first()
        vacancy_ref = response.url
        vacancy_source = response.css('div.bloko-column h4.supernova-footer-menu-header::text').extract_first()
        vacancy_city_1 = response.css('div.vacancy-company p:last-child::text').extract_first()
        vacancy_city2 = response.css('div.vacancy-company p:last-child span[data-qa="vacancy-view-raw-address"]::text').extract_first()
        if vacancy_city_1:
            vacancy_city = vacancy_city_1
        else:
            vacancy_city = vacancy_city2

        # print(vacancy_city)
        # print(salary_text)
        # print(salary_min)
        # print(salary_max)
        # print(vacancy_ref)
        # print(salary_currency)
        # print(vacancy_source)
        yield VacancyparserItem(name=name, vacancy_city=vacancy_city, salary_currency=salary_currency,
                                salary_max=salary_max, salary_min=salary_min, vacancy_ref=vacancy_ref,
                                vacancy_source=vacancy_source)

# /html/body/div[5]/div/div/div[2]/div/div/div[1]/div/div[1]/div[3]/div/div/div/div/p[2]/text()