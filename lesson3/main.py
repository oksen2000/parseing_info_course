import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
import json
from pymongo import MongoClient
import hashlib

# key_words = input("Введите ключевый слова")
key_words = "Разработчик Python"

# Сорри! это пока выше моих сил !!! Я доделаю, когда соберусь с духом!!
def parse_hh():
    link = "https://hh.ru/?customDomain=1"
    user_params = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    html = requests.get("https://hh.ru/?customDomain=1").text
    parsed_html = bs(html, 'lxml')
    vacancy_list = []

    for vacancy in vacancy_nodes:
        vacancy_data = {'name': name, 'link': link, 'salary_from': salary_from, 'salary_to': salary_to,
                        'currency': currency}
        vacancy_list.append(vacancy_data)

    return vacancy_list


def parse_super_job():
    main_sj_link = "https://russia.superjob.ru"
    link1 = main_sj_link + "/vacancy/search/?keywords="
    user_params = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

    html = requests.get(link1 + key_words.replace(" ", "%20"), params=user_params).text
    parsed_html = bs(html, 'lxml')
    vacancy_nodes = parsed_html.find_all('div', {'class':'_3mfro CuJz5 PlM3e _2JVkc _3LJqf'})

    vacancy_list = []

    for vacancy in vacancy_nodes:
        vacancy_data = {'name': name, 'link': link, 'salary_from': salary_from, 'salary_to': salary_to, 'currency': currency}
        vacancy_list.append(vacancy_data)

    return vacancy_list


# Пусть будет пока хотя бы dummy
def dummy_parse_vacancies():
    vacancy_list = []
    for i in range(5):
        vacancy_data = {}
        vacancy_data['name'] = "Super Vacancy(!!!) " + str(i)
        vacancy_data['link'] = f"http://dummy.ru/vacancy{i}"
        vacancy_data['salary_from'] = i * 40
        vacancy_data['salary_to'] = i * 50
        vacancy_data['currency'] = 'Руб'
        vacancy_list.append(vacancy_data)
    return vacancy_list


# Получим коллекцию вакансий
def get_vacancies():
    client = MongoClient('localhost', 27017)
    db = client['vacancies_db']
    return db.vacancies


def write_to_mongo(vacancies_list):
    vacancies = get_vacancies()
    for vac in vacancies_list:
        vac_link = vac.get('link')
        # Считаю ссылку на вакансию хорошим ключом, так как она на обоих сайтах содержит id вакансии
        # можно вырезать ID  и добавлять идентификактор сайта - источника
        # тогда исключим проблемы при измнении относительных путей на сайте
        # Для сравнения содержания вакансии используем хэш
        prev_verion_vac = vacancies.find({"link": vac_link})
        current_hash = hashlib.md5(json.dumps(vac, sort_keys=True).encode("utf-8")).hexdigest()
        if prev_verion_vac:
            old_hash = prev_verion_vac[0].get("hash")
            if current_hash != old_hash:
                vacancies.delete_one({"hash": old_hash})
                vac['hash'] = current_hash
                vacancies.insert_one(vac)
                #print("Замена")
        else:
            vac['hash'] = current_hash
            vacancies.insert_one(vac)


write_to_mongo(dummy_parse_vacancies())

#Запрос вакансий с зарплатой выше указанной
def print_vacancies_by_salary(salary):
    vacancies = get_vacancies()
    for vac in vacancies.find({"salary_from": {"$gt": salary}}):
        print(vac)

#salary = int(input("Введите желаемую зарплату:"))
#print_vacancies_by_salary(salary)
