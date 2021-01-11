import requests
from bs4 import BeautifulSoup

html_doc = requests.get('https://www.detik.com/terpopuler', params={'tag_from': 'wp_cb_mostPopular_more'})

soup = BeautifulSoup(html_doc.text, 'html.parser')

popular_area = soup.find(attrs={'class': 'grid-row list-content'})

# print(popular_area)

titles = popular_area.find_all(attrs={'class': 'media__title'});

# for a in titles:
#     print(a.text)

images = popular_area.find_all(attrs={'class': 'media__image'});

for i in images:
    print(i.find('a').find('img')['title'])