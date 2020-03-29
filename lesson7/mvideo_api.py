import requests
from lxml import html
import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['mvideo_api']
db.hits

User_Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
user_params = {
    'User-Agent': User_Agent
}

response = requests.get("https://www.mvideo.ru", headers=user_params)
tree = html.fromstring(response.text)

res = tree.xpath('//div[@data-init="ajax-category-carousel"][1]/div[@class="section"]/script')[0].text

goods_str = res[res.index('['):res.index( ']') + 1]

goods = json.loads(goods_str)

db.hits.insert_many(goods)