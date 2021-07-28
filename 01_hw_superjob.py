from bs4 import BeautifulSoup as bs
import requests

main_link = 'https://russia.superjob.ru/vacancy/search/?keywords=python'
headers = {
    'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
}


response = requests.get(main_link, headers=headers)
