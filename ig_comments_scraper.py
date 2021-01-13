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

    writer = csv.writer(open('{}/{}.csv'.format(result_dir, shortcode), 'w', newline=''))
    headers = ['User Name', 'Comment']
    writer.writerow(headers)

    while 1:
        variables = {
            'shortcode': shortcode,
            'first': 50,
            'after': end_cursor
        }

        params = {
            'query_hash': 'bc3296d1ce80a24b1b6e40b1e72903f5',
            'variables': json.dumps(variables)
        }

        resp_json = session.get(url, params=params).json()
        comments = {}
        # print(resp_json)

        try:
            comments = resp_json['data']['shortcode_media']['edge_media_to_parent_comment']['edges']
        except Exception as e:
            print(f'Error Get Resp {e}, Wait For 30s...')
            time.sleep(30)

        for c in comments:
            count += 1
            username = c['node']['owner']['username']
            comment = c['node']['text']
            print(count, username, comment)
            writer = csv.writer(
                open('{}/{}.csv'.format(result_dir, shortcode), 'a', newline='', encoding='utf-8'))
            data = [username, comment]
            writer.writerow(data)

        page_info = resp_json['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']
        has_next_page = page_info['has_next_page']
        if has_next_page:
            end_cursor = page_info['end_cursor']
        else:
            break

        time.sleep(2)
