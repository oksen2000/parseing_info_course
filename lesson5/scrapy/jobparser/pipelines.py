# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re


def parse_salary(item):
    item['salary_min'] = 0
    item['salary_max'] = 0
    item['salary_currency'] = "Рубли"
    lst = item['salary']
    num1, num2 = 0,0
    is_do = False

    for word in lst:
        new_str = re.sub(r'[^0-9.]+', r'', word)
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


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacansy_305

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        parse_salary(item)
        collection.insert_one(item)
        return item
