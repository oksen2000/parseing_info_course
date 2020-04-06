import requests
from bs4 import BeautifulSoup as bs
import re
from pymongo import MongoClient
import hashlib

client = MongoClient('localhost', 27017)
db = client['vacancies_db']
user_params = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}


def parse_hh():
    process_page_hh("https://hh.ru/search/vacancy?area=113&st=searchVacancy&text=python")

def process_page_hh(url):
    html = requests.get(url, headers=user_params).text
    parsed_html = bs(html, 'lxml')

    next_page_button = parsed_html.find('a', {'class': 'HH-Pager-Controls-Next'})
    if next_page_button:
        next_page_link = "https://hh.ru" + next_page_button['href']

    vac_link_list = parsed_html.find_all('a', {'class': 'bloko-link HH-LinkModifier'})

    for item in vac_link_list:
        vac_data = {}
        link = item['href']
        html = requests.get(link, headers=user_params).text
        parsed_html = bs(html, 'lxml')
        name = parsed_html.find('h1', {'class': 'bloko-header-1'}).getText()
        salary = parsed_html.find('span', {'class': 'bloko-header-2 bloko-header-2_lite'}).getText()
        vac_data["source"] = "hh.ru"
        vac_data["url"] = link
        vac_data["name"] = name
        vac_data["salary"] = salary
        parse_salary(vac_data)
        db.vacancies.insert_one(vac_data)

    print("Обработана страница " + url)

    if next_page_button:
        process_page_hh(next_page_link)


def parse_salary(item):
    item['salary_min'] = 0
    item['salary_max'] = 0
    item['salary_currency'] = "Рубли"
    lst = item['salary'].split(" ")
    num1, num2 = 0,0
    is_do = False

    for word in lst:
        new_str = re.sub(r'[^0-9]+', r'', word)
        if new_str != '':
            if num1 == 0:
                num1 = int(new_str)
            elif num2 == 0:
                num2 = int(new_str)
        if "до" in word:
            is_do = True

    if (num1 > 0) & (num2 > 0):
        item['salary_min'] = num1
        item['salary_max'] = num2
    elif (num2 == 0) & is_do:
        item['salary_max'] = num1
    else:
        item['salary_min'] = num1


    if lst.count('EUR') > 0:
        item['salary_currency'] = 'EUR'

    if lst.count('USD') > 0:
        item['salary_currency'] = 'USD'


def parse_sj():
    process_page_sj("https://russia.superjob.ru/vacancy/search/?keywords=python")

def process_page_sj(url):
    html = requests.get(url, headers=user_params).text
    parsed_html = bs(html, 'lxml')

    next_page_button = parsed_html.find('a', {'class': 'f-test-link-Dalshe'})
    if next_page_button:
        next_page_link = "https://russia.superjob.ru" + next_page_button['href']

    vac_link_list = parsed_html.find_all('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'})

    for item in vac_link_list:
        item_a = item.find('a')
        if item_a:
            link = "https://russia.superjob.ru" + item_a['href']
            vac_data = {}
            html = requests.get(link, headers=user_params).text
            parsed_html = bs(html, 'lxml')
            name = parsed_html.find('h1', {'class': '_3mfro rFbjy s1nFK _2JVkc'}).getText()
            salary = parsed_html.find('span', {'class': '_3mfro _2Wp8I ZON4b PlM3e _2JVkc'}).getText()
            vac_data["source"] = "superjob.ru"
            vac_data["url"] = link
            vac_data["name"] = name
            vac_data["salary"] = salary
            parse_salary(vac_data)
            db.vacancies.insert_one(vac_data)

    print("Обработана страница " + url)

    if next_page_button:
        process_page_sj(next_page_link)



parse_sj()
parse_hh()

