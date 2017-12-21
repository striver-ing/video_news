# -*- coding: utf-8 -*-
'''
Created on 2017-12-21 10:13
---------
@summary:
---------
@author: Boris
'''


import base.base_parser as base_parser
import utils.tools as tools
from utils.log import log

SITE_ID = 1712200006
NAME = '腾讯'


# 必须定义 添加网站信息
@tools.run_safe_model(__name__)
def add_site_info():
    log.debug('添加网站信息')

    table = 'VIDEO_NEWS_site_info'
    url = 'https://v.qq.com'

    base_parser.add_website_info(table, site_id=SITE_ID, url=url, name=NAME)


# 必须定义 添加根url
@tools.run_safe_model(__name__)
def add_root_url(keywords):
    log.debug('''
        添加根url
        parser_params : %s
        ''' % str(keywords))
    for keyword in keywords:
        next_keyword = False
        for page_index in range(1, 10):
            keyword = tools.quote(keyword)
            url = 'https://v.qq.com/x/search/?q=%s&filter=sort=1&&cur=%s' % (keyword, page_index)
            html, res = tools.get_html_by_requests(url)
            video_list_title = tools.get_tag(html, 'div', {'class': 'result_item'})
            if not video_list_title:
                break
            for info_index, video_info in enumerate(video_list_title):
                try:
                    image_url = tools.get_tag(video_info, 'img', find_all=False)['src']
                    image_url = 'http:' + image_url
                    title = tools.get_tag(video_info, 'h2', find_all=False).get_text()
                    url = tools.get_tag(video_info, 'h2', find_all=False).a['href']
                    release_time = tools.get_tag(video_info, 'span', {'class': 'content'}, find_all=False).get_text()
                except:
                    continue
                current_date = tools.get_current_date('%Y-%m-%d')
                if current_date > release_time:
                    next_keyword = True
                    break
                base_parser.save_video_info(image_url=image_url, url=url, title=title, release_time=release_time,
                                            site_name=NAME)
            if next_keyword:
                break


# 必须定义 解析网址
def parser(url_info):
    pass
