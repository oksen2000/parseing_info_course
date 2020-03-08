import requests
import json

username = input("Введите логин:\n")
password = input("Введите пароль:\n")

repos = requests.get('https://api.github.com/user/repos', auth=(username, password))

with open('data.json', 'w') as f:
    json.dump(repos.json(), f)

for repo in repos.json():
    if not repo['private']:
        print(repo['html_url'])

