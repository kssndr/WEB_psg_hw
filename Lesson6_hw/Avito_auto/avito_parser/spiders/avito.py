# -*- coding: utf-8 -*-
import scrapy
from avito_parser.items import AvitoParserItem
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/sankt-peterburg/avtomobili/s_probegom/opel/vnedorozhnik/avtomat?radius=0']

    def parse(self, response):
        next_page = response.css('a[class="pagination-page js-pagination-next"]::attr(href)').extract_first()
        print(next_page)
        yield response.follow(next_page, callback=self.parse)

        ads_link = response.css('a[class="item-description-title-link"]::attr(href)').extract()
        print(len(ads_link))
        for link in ads_link:
            yield response.follow(link, self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoParserItem(), response=response)
        loader.add_css('title', 'h1.title-info-title span.title-info-title-text::text')
        loader.add_css('price', 'span.js-item-price::text')
        loader.add_xpath('parameters', '//ul[contains(@class,"item-params-list")]//li[contains(@class, '
                                   '"item-params-list-item")]')
        loader.add_xpath('photos', '//div[contains(@class,"gallery-img-wrapper")]//div[contains(@class, '
                                   '"gallery-img-frame")]/@data-url')
        yield loader.load_item()
