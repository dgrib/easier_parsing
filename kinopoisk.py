from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
main_link = 'https://www.kinopoisk.ru'
response = requests.get(f'{main_link}/premiere/').text
soup = bs(response, 'lxml')

films_block = soup.find_all('div', {'class': 'prem_list'})[1]  # так как 2 таких элемента с классом

films_list = films_block.find_all('div', {'class': 'premier_item'})
# films_list = films_block.findChildren(recursive=False)[1:]  # можно и так

films = []
for film in films_list:
    film_data = {}
    main_data = film.find('span')
    film_data['name'] = main_data.getText()
    film_data['link'] = main_link + main_data.findChild()['href']  # к зеачениям атрибута можно обращаться как к ключам словаря
    film_data['genre'] = main_data.find_next_siblings()[-2].getText()  # всех соседей, но так делать не хорошо вдруг изменится

    print(film_data)

    films.append(film_data)

pprint(films)
