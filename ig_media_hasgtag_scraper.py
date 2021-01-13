import time

from ig_login import login


# MAIN FUNCTION
session = login()
result_dir = 'ig_scraper_results'
if session is not None:
    end_cursor = ''
    count = 0
    while True:
        url_hashtag = 'https://www.instagram.com/explore/tags/villamelatimasbsd/?__a=1&max_id={}'.format(end_cursor)
        resp_json = session.get(url_hashtag).json()
        shortcodes = resp_json['graphql']['hashtag']['edge_hashtag_to_media']['edges']

        for sc in shortcodes:
            time.sleep(2)
            shortcode = sc['node']['shortcode']
            url_detail = 'https://www.instagram.com/p/{}/?__a=1'.format(shortcode)
            resp_detail = session.get(url_detail).json()
            username = resp_detail['graphql']['shortcode_media']['owner']['username']
            count += 1
            is_video = resp_detail['graphql']['shortcode_media']['is_video']
            if is_video:
                file_name_video = '{} {}.mp4'.format(count, username)
                path_video = '{}/{}'.format(result_dir, file_name_video)
                url_media_video = resp_detail['graphql']['shortcode_media']['video_url']
                # print(url_media_video)
                resp_url_media_video = session.get(url_media_video).content
                open(path_video, 'wb').write(resp_url_media_video)
            else:
                file_name_image = '{} {}.jpg'.format(count, username)
                path_image = '{}/{}'.format(result_dir, file_name_image)
                url_media_image = resp_detail['graphql']['shortcode_media']['display_url']
                resp_url_media_image = session.get(url_media_image).content
                open(path_image, 'wb').write(resp_url_media_image)
            print(count, shortcode)

        end_cursor = resp_json['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        has_next_page = resp_json['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']

        if not has_next_page: break
        time.sleep(2)
