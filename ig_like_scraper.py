import csv
import json
import os
import time
from ig_login import login


# MAIN FUNCTION
session = login()
result_dir = 'ig_scraper_results'
if session is not None:
    # shortcode = 'CJ5ZaEfMMmi'
    shortcode = input('Input shortcode: ')

    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    url = 'https://www.instagram.com/graphql/query'
    end_cursor = ''
    count = 0

    csv_file = open('{}/{}.csv'.format(result_dir, shortcode), 'w', newline='')
    writer = csv.writer(csv_file)
    headers = ['User Name', 'Full Name', 'Profile Pict']
    writer.writerow(headers)
    csv_file.close()
    csv_file = open('{}/{}.csv'.format(result_dir, shortcode), 'a', newline='', encoding='utf-8')
    writer = csv.writer(csv_file)

    while 1:
        variables = {
            'shortcode': shortcode,
            'first': 50,
            'after': end_cursor
        }

        params = {
            'query_hash': 'd5d763b1e2acf209d62d22d184488e57',
            'variables': json.dumps(variables)
        }

        resp_json = session.get(url, params=params).json()
        users = {}
        # print(resp_json)

        try:
            users = resp_json['data']['shortcode_media']['edge_liked_by']['edges']
        except Exception as e:
            print(f'Error Get Resp {e}, Wait For 30s...')
            time.sleep(30)

        for user in users:
            count += 1
            username = user['node']['username']
            full_name = user['node']['full_name']
            profile_pic_url = user['node']['profile_pic_url']
            print(count, username, full_name, profile_pic_url)
            data = [username, full_name, profile_pic_url]
            writer.writerow(data)

        page_info = resp_json['data']['shortcode_media']['edge_liked_by']['page_info']
        has_next_page = page_info['has_next_page']
        if has_next_page:
            end_cursor = page_info['end_cursor']
        else:
            break

        time.sleep(2)

    csv_file.close()