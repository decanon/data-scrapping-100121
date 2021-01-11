import glob
import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

session = requests.Session()


def login():
    print('login...')
    data_login = {
        'username': 'user',
        'password': 'user12345'
    }

    res = session.post('http://127.0.0.1:5000/login', data=data_login)
    soup = BeautifulSoup(res.text, 'html.parser')

    page_items = soup.find_all('li', attrs={'class': 'page-item'})
    total_pages = len(page_items) - 2

    return total_pages


def get_urls(page):
    print(f'get urls... page={page}')

    params = {
        'page': page
    }

    res = session.get('http://127.0.0.1:5000', params=params)
    soup = BeautifulSoup(res.text, 'html.parser')

    # soup = BeautifulSoup(open('./res.html'), 'html.parser')

    titles = soup.find_all('h4', attrs={'class': 'card-title'})
    urls = []
    for title in titles:
        url = title.find('a')['href']
        urls.append(url)

    # print(urls)
    # f = open('./res.html', 'w+')
    # f.write(res.text)
    # f.close()

    return urls


def get_details(url):
    print(f'get details... url={url}')

    res = session.get('http://127.0.0.1:5000'+url)

    # f = open('./res.html', 'w+')
    # f.write(res.text)
    # f.close()

    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.find('title').text.strip()
    price = soup.find('h4', attrs={'class': 'card-price'}).text.strip()
    stock = soup.find('span', attrs={'class': 'card-stock'}).text.strip().replace('stock: ', '')
    category = soup.find('span', attrs={'class': 'card-category'}).text.strip().replace('category: ', '')
    description = soup.find('p', attrs={'class': 'card-text'}).text.strip().replace('Description: ', '')

    dict_data = {
        'title': title,
        'price': price,
        'stock': stock,
        'category': category,
        'description': description
    }

    with open('./rwid_scraper_results/{}.json'.format(url.replace('/', '')), 'w') as outfile:
        json.dump(dict_data, outfile)


def create_csv():
    # use glob to create csv

    files = sorted(glob.glob('./rwid_scraper_results/*.json'))
    datas = []
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)

    df = pd.DataFrame(datas)
    df.to_csv('./rwid_scraper_results/results.csv', index=False)
    print('csv generated...')


def run():
    total_pages = login()

    if not os.path.exists('rwid_scraper_results'):
        os.mkdir('rwid_scraper_results')

    options = 1
    while 1 <= options <= 3:
        options = int(input('1. Collecting all urls\n2. Get detail all products\n3. Create CSV\nInput Option Number: '))

        if options == 1:
            total_urls = []
            for i in range(total_pages):
                urls = get_urls(i + 1)
                total_urls += urls
            with open('./rwid_scraper_results/all_urls.json', 'w') as outfile:
                json.dump(total_urls, outfile)
            # print(total_urls)
            # print(len(total_urls))
        elif options == 2:
            with open('./rwid_scraper_results/all_urls.json') as json_file:
                all_url = json.load(json_file)
            # print(all_url)
            for url in all_url:
                get_details(url)
        elif options == 3:
            create_csv()
        else:
            break


if __name__ == '__main__':
    run()
