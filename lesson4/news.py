import requests
from pprint import pprint
from lxml import html
from pymongo import MongoClient


User_Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
user_params = {
    'User-Agent': User_Agent}
client = MongoClient('localhost', 27017)
db = client['news_db']
db.news_collection


def parse_lenta():
    main_link = 'https://www.lenta.ru'
    response = requests.get(main_link, params=user_params).text
    tree = html.fromstring(response)

    news_block = tree.xpath("//section[@class='row b-top7-for-main js-top-seven']")
    new_list = news_block[0].xpath(".//div[@class='item']")

    news_list_to_db = []
    for news_item in new_list:
        news_items_dict = {}
        news_items_dict['source'] = "lenta.ru"
        news_items_dict['text'] = news_item.xpath(".//a/text()")[0]
        news_items_dict['time'] = news_item.xpath(".//a/time/@datetime")[0]
        news_items_dict['href'] = main_link + news_item.xpath(".//a/@href")[0]
        news_list_to_db.append(news_items_dict)

    db.news_collection.insert_many(news_list_to_db)


def parse_mail():
    main_link = 'https://news.mail.ru/'
    response = requests.get(main_link, params=user_params).text
    tree = html.fromstring(response)

    link_list = []
    #Соберем сначала ссылки
    #Главная новость
    link_list = link_list + tree.xpath("//a[@class='photo photo_full photo_scale js-topnews__item']/@href")
    #Новости с картинками
    link_list = link_list + tree.xpath("//td[@class='daynews__items']//div//a/@href")
    #Новости без картинок
    link_list = link_list + tree.xpath("//ul[@name='clb20268353']//li//a/@href")
    for link in link_list:
        process_one_new_mail(main_link + link)


def process_one_new_mail(link):
    try:
        response = requests.get(link, params=user_params).text
        tree = html.fromstring(response)
        news_items_dict = {}
        news_items_dict['source'] = tree.xpath("//a[@class='link color_gray breadcrumbs__link']//span[@class='link__text']/text()")[0]
        news_items_dict['text'] = tree.xpath("//h1[@class='hdr__inner']/text()")[0]
        news_items_dict['time'] = tree.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0]
        news_items_dict['href'] = link
        db.news_collection.insert_one(news_items_dict)
    except:
        pass


def parse_yandex():
    main_link = 'https://yandex.ru'
    response = requests.get(main_link + "/news", params=user_params).text
    tree = html.fromstring(response)

    news_list = tree.xpath("//div[@class='story story_view_short story_notags']")[:10]
    for root in news_list:
        news_items_dict = {}
        source_and_time = root.xpath(".//div[@class='story__date']/text()")[0]
        time = source_and_time.split(' ')[-1]
        news_items_dict['time'] = time
        news_items_dict['source'] = source_and_time.replace(time, "")
        news_items_dict['href'] = main_link + root.xpath(".//a[contains(@class,'link link_theme_black')]/@href")[0]
        news_items_dict['text'] = root.xpath(".//a[contains(@class,'link link_theme_black')]/text()")[0]
        db.news_collection.insert_one(news_items_dict)


db.news_collection.delete_many({})
parse_lenta()
parse_mail()
parse_yandex()




