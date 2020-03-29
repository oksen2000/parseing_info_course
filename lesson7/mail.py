from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['mail']
db.drop_collection("inbox")

driver = webdriver.Chrome()


driver.get('https://mail.ru/')
assert "Mail" in driver.title

try:
    elem = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.ID,'mailbox:login')))
    elem.clear()
    elem.send_keys('study.ai_172')

    elem =  WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,"//input[@class='o-control']")))
    elem.click()

    elem = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.ID, "mailbox:password")))
    elem.send_keys('NewPassword172')
    elem.send_keys(Keys.RETURN)

    a_set = set()
    a_list = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH,"//a[contains(@class,'js-letter-list-item')]")))
    a_set.update([item.get_attribute("href") for item in a_list])

    old_size = len(a_set)
    while len(a_list) > 0:
        try:
            a_list[-1].send_keys(Keys.PAGE_DOWN)
            a_list = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH,"//a[contains(@class,'js-letter-list-item')]")))
            a_set.update([item.get_attribute("href") for item in a_list])
        except Exception as e:
            print('При выполнении поизошла ошибка: ', e)
            break
        if len(a_set) == old_size:
            break
        old_size = len(a_set)

    print(f"Найдено {len(a_set)} писем ")

    for link in a_set:
        try:
            letter_data = {}
            driver.get(link)
            letter_data['subject'] = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[@class='thread__subject']"))).text
            letter_data['date'] = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='letter__date']"))).text
            letter_data['from'] = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='letter-contact']"))).get_attribute("title")
            letter_data['body'] = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='letter-body__body-content']"))).text
            db.inbox.insert_one(letter_data)
        except:
            continue

except Exception as e:
    print('При выполнении поизошла ошибка: ', e)
finally:
    driver.quit()



