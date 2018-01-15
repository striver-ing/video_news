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
from extractor.article_extractor import ArticleExtractor
import base.constance as Constance

SITE_ID = 1712200004
NAME = '新浪'


# 必须定义 添加网站信息
@tools.run_safe_model(__name__)
def add_site_info():
    log.debug('添加网站信息')

    table = 'VIDEO_NEWS_site_info'
    url = 'http://video.sina.com.cn/'

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
            url = 'http://so.video.sina.com.cn/interface/s?from=video&wd=%s&s_id=w00001&p=%s&n=20&s=1' \
                  % (keyword, page_index)
            info_json = tools.get_json_by_requests(url)
            video_info_list = info_json['list']
            if not video_info_list:
                print(url)
                break
            for video_info in video_info_list:
                image_url = video_info['thumburl']
                title = tools.del_html_tag(video_info['videoname'])
                url = video_info['url']
                release_time = video_info['showtime']

                is_continue = base_parser.save_video_info(image_url=image_url, url=url, title=title, release_time=release_time,
                                            site_name=NAME)
                if not is_continue:
                    next_keyword = True
                    break

            if next_keyword:
                break


# 必须定义 解析网址
def parser(url_info):
    pass