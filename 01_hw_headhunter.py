import json
from datetime import datetime

from bs4 import BeautifulSoup as bs
import requests
from time import sleep
import re


def salary_processing(text):
    """Получает зарплату в виде строки '40000–120000руб.', возвращает кортеж вида ('от', 'до', 'валюта')"""
    new_text = text.split()  # убираю пробельные символы
    new_text = ''.join(new_text)  # объединяю список в строку без пробельных символов
    result_list = list(re.findall(r'([а-я]{2})?(\d+)[–]?(\d*)([A-Z|руб.]+)', new_text)[0][1:])
    result_list = [i if i else None for i in result_list]
    return tuple(result_list) if 'до' not in text else (result_list[1], result_list[0], result_list[2])


def save_to_json_txt(data_list):
    with open(f'parse_data_{datetime.now().date()}.txt', 'w') as file:
        json.dump(data_list, file)


# main_link = 'https://perm.hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text=python'
main_link = 'https://perm.hh.ru/search/vacancy?' \
            'clusters=true&enable_snippets=true&text=python&L_save_area=true&area=1317&showClusters=true&'
headers = {
    'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
}

offers = []  # хранит список вакансий
quit_marker = True  # выход из цикла, если нет кнопки "Дальше"
page_number = 0  # страница на hh передает в headers
while quit_marker:
    sleep(2)
    response = requests.get(f'{main_link}&page={page_number}', headers=headers).text
    soup = bs(response, 'lxml')
    # offers_block = soup.find('div', {'data-qa': 'vacancy-serp__results'})

    offers_list = soup.find_all('div', {'class': 'vacancy-serp-item'})
    print(len(offers_list))

    for offer in offers_list:
        offer_data = {}
        main_data = offer.find('a')
        offer_data['name'] = main_data.getText()
        offer_data['link'] = main_data['href']
        offer_data['description'] = offer.find('div', {'class': 'g-user-content'}).getText()
        try:
            salary = offer.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
        except AttributeError:
            offer_data['salary_min'] = None
            offer_data['salary_max'] = None
            offer_data['salary_currency'] = None
        else:
            offer_data['salary_min'], offer_data['salary_max'], offer_data['salary_currency'] = salary_processing(salary)

        print(offer_data)
        offers.append(offer_data)

    page_number += 1
    if not soup.find('a', {'data-qa': 'pager-next'}):
        quit_marker = False

save_to_json_txt(offers)





# python
#
# name
# link
# description
# salary
#
# нажимаем пегинацию page=1
# или пока нет кнопки дальше
#
# статус код проверять
#
# user_agent надо передавать на hh
#
#
# superjob.ru
#
# кастомизироваь программу - пусть спрашивает какой тег искать python или ...
# нажимаем пегинацию page=1
# или пока нет кнопки дальше
#
# проверка выхода из цикла "по заданным параметрам ..."
#
# Обработку ЗП написать
# Когда ЗП нет ставим None
# Есть от...
# Есть до ...
# рубли доллары
#
# ЗП разделить на три составляющие
# ьин макс и валюта
#
# None или число int
# 2-31-31 время для задания
