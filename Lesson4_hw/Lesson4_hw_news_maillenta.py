"""
Задание 4:
Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать xpath. Структура данных должна содержать:
• название источника,
• наименование новости,
• ссылку на новость,
• дата публикации

"""


from lxml import html
import requests
from pprint import pprint
import datetime


header = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                        "Version/13.0.3 Safari/605.1.15"}
main_link_mail = "https://mail.ru"
main_link_lenta = "https://lenta.ru"
main_link_yandex = "https://yandex.ru"
all_news = []
news_list = {}


def get_news_mail():
    req = requests.get(main_link_mail, headers=header)
    root = html.fromstring(req.text)
    name_list = root.xpath("//div[@class='news-item__inner']/a[last()]/text()|//h3[@class='news-item__title i-link-deco']/text()")
    ref_list = root.xpath(
        "//div[@class='news-item__inner']/a[last()]/@href|//div[@class='news-item o-media news-item_media news-item_main']/a/@href")
    # print(len(name_list))

    for news in range(len(name_list)):
        news_list["id_news"] = "m"+(datetime.datetime.today()).strftime("%Y%m%d%H%M")+"-" + str(news)
        news_list["source"] = "mail.ru"
        news_list["name"] = name_list[news].replace("\xa0", " ")
        news_list["ref"] = ref_list[news]
        news_list["news_date"] = (datetime.datetime.today()).strftime("%H:%M, %d %m %Y")
        all_news.append(news_list.copy())
    return


def get_news_lenta():
    req = requests.get(main_link_lenta, headers=header)
    root = html.fromstring(req.text)
    name_list = root.xpath(
        '//div[@class="span4"]/div[@class ="first-item"]/h2/a/text()|//div[@class="span4"]/div[@class ="item"]/a/text()')
    ref_list = root.xpath(
        '//div[@class="span4"]/div[@class ="first-item"]/h2/a/@href|//div[@class="span4"]/div[@class ="item"]/a/@href')
    date_list = root.xpath(
        '//div[@class="span4"]/div[@class ="first-item"]/h2/a/time/@datetime|//'
        'div[@class="span4"]/div[@class ="item"]/a/time/@datetime')
    len(name_list)
    for news in range(len(name_list)):
        news_list["id_news"] = "l"+(datetime.datetime.today()).strftime("%Y%m%d%H%M")+"-" + str(news)
        news_list["source"] = "lenta.ru"
        news_list["name"] = name_list[news].replace("\xa0", " ")
        news_list["ref"] = main_link_lenta+ref_list[news]
        news_list["news_date"] = date_list[news]
        all_news.append(news_list.copy())
    return


def get_news_yandex():
    req = requests.get(main_link_yandex, headers=header)
    root = html.fromstring(req.text)
    name_list = root.xpath(
        '//span[@class="news__item-content"]/text()')
    ref_list = root.xpath(
        '//ol[@class="list news__list"]/li/a/@href | //ol[@class="list news__list news__animation-list"]/li/a/@href')
    print(len(name_list))
    for news in range(len(name_list)):
        news_list["id_news"] = "y"+(datetime.datetime.today()).strftime("%Y%m%d%H%M")+"-" + str(news)
        news_list["source"] = "yandex.ru"
        news_list["name"] = name_list[news].replace("\xa0", " ")
        news_list["ref"] = main_link_lenta+ref_list[news]
        news_list["news_date"] = (datetime.datetime.today()).strftime("%H:%M, %d %m %Y")
        all_news.append(news_list.copy())
    return


get_news_mail()
get_news_lenta()
get_news_yandex()
pprint(all_news)
