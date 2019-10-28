from pprint import pprint
from lxml import html
import requests
header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

def requests_to_yandex(str):
    req = requests.get('https://yandex.ru/search/',
                            params={'text':str},
                            headers=header)
    root = html.fromstring(req.text)
    result_list = root.xpath("//a[contains(@class,'link_cropped_no')]/@href | "
                             "//a[contains(@class,'organic__url_type_multiline')]/@href")
    if result_list:
        for i in result_list:
            print(i)
    else:
        print(f'{str} not found')

requests_to_yandex('Суши')


