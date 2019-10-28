# Задание:
# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайта
# superjob.ru и hh.ru. Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
#     *Наименование вакансии
#     *Предлагаемую зарплату (отдельно мин. и отдельно макс.)
#     *Ссылку на саму вакансию
#     *Сайт откуда собрана вакансия
# По своему желанию можно добавить еще работодателя и расположение. Данная структура должна быть одинаковая для вакансий
# с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.
#
#
# Алгоритм:
# принять название искомой должности и количество необходимых вакансий
# Сохранить страницу HH и SJ
#
###


from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests
import time
from random import randint
from trans import trans

# функция разделения предложения размера зп на мин и макс
def compensation_min_max(compensation):
    c = str(compensation).replace("\xa0"," ")
    if c[:2] == "По":
        minimum = "По договорённости"
        maximum = "По договорённости"
    elif c[:2] == "от":
        minimum = c[3:].replace("\xa0","")
        maximum = "По договорённости"
    elif c[:2] == "до":
        minimum = "По договорённости"
        maximum = c[3:].replace("\xa0", "")
    elif "-" in c:
        minimum, maximum = c.split("-")
    else:
        minimum = c
        maximum = c

    return minimum, maximum


# запрос вводных
order_vacancy_name = input("Введите интересующую вакансию: ")
quantity = int(input("Какое количество вакансий по каждому ресурсу показать: "))

# конвертация названия вакансии для сайта superjob
order_vacancy_name_for_sj = trans(order_vacancy_name).replace("'", "").replace(" ", "-")
# print(order_vacancy_name_for_sj)

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

#загрузка файла с первой страницей
# html_hh = open('hh.html', 'r')

# создания DOM
# parsed_html_hh = bs(html_hh, 'lxml')

# загрузка блока с вакансиями и создание списка блоков с нужной информацией
# vacancy_block = parsed_html_hh.find('div', {'class': 'vacancy-serp'})
# vacancy_list = vacancy_block.findChildren(recursive=False)

# vacancies = []
vacancies_counter_hh = 0
vacancies_counter_sj = 0
page_hh = 0
page_sj = 1
vacancies = []

# организация сбора информации с сайта hh
while vacancies_counter_hh < quantity:
    next_page_hh = "https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_" \
                   "snippets=true&search_field=name&text="
    html_hh = requests.get(next_page_hh + order_vacancy_name + "&" + str(page_hh), headers=header).text

    # код для отладки (для сохранения файл убрать .text
    # with open(f'hh_{page_hh}.html', 'wb') as file:
    #     file.write(html_hh.content)
    #
    # html_hh = open(f'hh_{page_hh}.html', 'r')

    parsed_html_hh = bs(html_hh, 'lxml')
    vacancy_block = parsed_html_hh.find('div', {'class': 'vacancy-serp'})

    # проверка наличия вакансий на странице (то что они есть или не кончились)
    if vacancy_block:
        vacancy_list = vacancy_block.findChildren(recursive=False)
    else:
        break
    #  цикл сбора данных
    for vacancy in vacancy_list:
        vacancy_data = {}
        main_info = vacancy.find('a', {"class": "bloko-link HH-LinkModifier"})
        if main_info:
            vacancy_name = main_info.getText()
            # print(vacancy_name)
            vacancy_link = main_info["href"]
            # print(vacancy_link)
            main_info = vacancy.find('div', {"class": "vacancy-serp-item__compensation"})
            if main_info:
                vacancy_compensation_min, vacancy_compensation_max = compensation_min_max(main_info.getText())
                # print(vacancy_compensation_min, "\n", vacancy_compensation_max)
            else:
                vacancy_compensation = "По договоренности"
                vacancy_compensation_min, vacancy_compensation_max = compensation_min_max(vacancy_compensation)
                # print("Договорная")
            main_info = vacancy.find('div', {"class": "vacancy-serp-item__meta-info"}).findChild()
            company_name = main_info.getText()
            # print(company_name)
            main_info = vacancy.find('span', {"data-qa": "vacancy-serp__vacancy-address"})
            vacancy_address = main_info.getText()
            # print(vacancy_address)

            if vacancies_counter_hh < quantity:
                vacancy_data['source'] = "HH"
                vacancy_data['name'] = vacancy_name
                vacancy_data['salary_min'] = vacancy_compensation_min
                vacancy_data['salary_max'] = vacancy_compensation_max
                vacancy_data['link'] = vacancy_link
                vacancy_data['company'] = company_name
                vacancy_data['city'] = vacancy_address
                vacancies.append(vacancy_data)
            else:
                break
            # подсчет обработанных вакансий
            vacancies_counter_hh += 1
    # определение стоит ли дальше делать запрос на новую страницу (если вакансий обработано меньше 20
    # значит они закончились
    if vacancies_counter_hh < quantity and vacancies_counter_hh == 20:
        page_sj += 1
        time.sleep(randint(3, 5))
    else:
        break

# организация сбора информации с сайта sj
while vacancies_counter_sj < quantity:
    if page_sj == 1:
        next_page_sj = "https://www.superjob.ru/vakansii/"
        add = ".html"
    else:
        next_page_sj = "https://www.superjob.ru/vakansii/"
        add = f".html?page={page_sj}"

    html_sj = requests.get(next_page_sj + order_vacancy_name_for_sj + add, headers=header).text

    # код для отладки (для сохранения файл убрать .text
    # with open(f'sj_{page_sj}.html', 'wb') as file:
    #     file.write(html_sj.content)
    #
    # html_sj = open(f'sj_{page_sj}.html', 'r')

    parsed_html_sj = bs(html_sj, 'lxml')
    vacancy_block = parsed_html_sj.find('div', {'style': 'display:block'})

    # проверка наличия вакансий на странице (то что они eсть или не кончились)
    if vacancy_block:
        vacancy_list = vacancy_block.findChildren(recursive=False)
    else:
        break

    for vacancy in vacancy_list:
        vacancy_data = {}
        if vacancy['class'] == ['_3zucV', '_2GPIV', 'f-test-vacancy-item', 'i6-sc', '_3VcZr']:
            vacancy_name = vacancy.find("div", {"class": "_3mfro CuJz5 PlM3e _2JVkc _3LJqf"}).getText()
            # print(vacancy_name)
            vacancy_link = "https://www.superjob.ru"+vacancy.find("a")['href']
            # print(vacancy_link)
            company_name = vacancy.find("span", {
                'class': "_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _3e53o _15msI"})
            if company_name: # изменил
                company_name = vacancy.find("span", {
                    'class': "_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _3e53o _15msI"})\
                    .getText()
                # print(company_name)
            else:
                company_name = "информация доступна на собеседовании"
            vacancy_address = \
                vacancy.find_all("span", {'class': '_3mfro f-test-text-company-item-location _9fXTd _2JVkc _3e53o'})[
                    0].getText().split("•")[1]
            # print(vacancy_address)
            compensation = \
                vacancy.find_all("span",
                                 {'class': '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'})[
                    0].getText().replace("—", "-")
            # print(compensation)
            vacancy_compensation_min, vacancy_compensation_max = compensation_min_max(compensation)

            if vacancies_counter_sj < quantity:
                vacancy_data['source'] = "SJ"
                vacancy_data['name'] = vacancy_name
                vacancy_data['salary_min'] = vacancy_compensation_min
                vacancy_data['salary_max'] = vacancy_compensation_max
                vacancy_data['link'] = vacancy_link
                vacancy_data['company'] = company_name
                vacancy_data['city'] = vacancy_address
                vacancies.append(vacancy_data)
            else:
                break

            vacancies_counter_sj += 1
    # определение стоит ли дальше делать запрос на новую страницу (если вакансий обработано меньше 20
    # значит они закончились
    if vacancies_counter_sj < quantity and vacancies_counter_sj == 20:
        page_sj += 1
        time.sleep(randint(3, 5))
    else:
        break

pprint(vacancies)

# проверка работы счетчиков
print("Итого вакансий с HH: ", vacancies_counter_hh)
print("Итого вакансий с SJ: ", vacancies_counter_sj)
# print(page_hh)
# print(page_sj)


