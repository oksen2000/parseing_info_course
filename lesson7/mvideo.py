from selenium import webdriver
from pymongo import MongoClient
import json

client = MongoClient('localhost', 27017)
db = client['mvideo']
db.drop_collection("hits")

driver = webdriver.Chrome()

driver.get('https://www.mvideo.ru/')
driver.maximize_window()
assert "М.Видео" in driver.title


try:
    elem = driver.find_elements_by_xpath("//div[@class='gallery-content accessories-new ']")[0]
    btn_lst = elem.find_elements_by_xpath("//div[@class='gallery-content accessories-new '][1]//a[@class='next-btn sel-hits-button-next']")
    while len(btn_lst) == 3:
        try:
            btn_lst[0].click()
            btn_lst = elem.find_elements_by_xpath(
                "//div[@class='gallery-content accessories-new '][1]//a[@class='next-btn sel-hits-button-next']")
        except:
            break

    elem = driver.find_elements_by_xpath("//div[@class='gallery-content accessories-new ']")[0]
    list = elem.find_elements_by_xpath(".//li[@class='gallery-list-item']//div[@class='c-product-tile-picture__holder']//a")

    for item in list:
        if item.get_attribute("data-product-info"):
            good = json.loads(item.get_attribute("data-product-info"))
            db.hits.insert_one(good)

except Exception as e:
    print('При выполнении поизошла ошибка: ', e)
finally:
    driver.quit()






