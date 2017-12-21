# -*- coding: utf-8 -*-
'''
Created on 2017-12-21 10:14
---------
@summary:
---------
@author: Boris
'''


import base.base_parser as base_parser
import utils.tools as tools
from utils.log import log

SITE_ID = 1712200007
NAME = '优酷'


def get_release_time(release_time):
    try:
        if '小时前' in release_time:
            print(release_time)
            nhours = tools.re.compile('(\d+)小时前').findall(release_time)
            hours_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(hours=int(nhours[0])))
            release_time = hours_ago.strftime("%Y-%m-%d %H:%M")
        elif tools.re.compile('分钟前').findall(release_time):
            nminutes = tools.re.compile('(\d+)分钟前').findall(release_time)
            minutes_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(minutes=int(nminutes[0])))
            release_time = minutes_ago.strftime("%Y-%m-%d %H:%M")
        else:
            release_time = ''
    except:
        release_time = ''
    finally:
        return release_time


# 必须定义 添加网站信息
@tools.run_safe_model(__name__)
def add_site_info():
    log.debug('添加网站信息')

    table = 'VIDEO_NEWS_site_info'
    url = 'http://www.soku.com'

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
            url = 'http://www.soku.com/search_video/q_%s_orderby_2_limitdate_0?spm=a2h0k.8191407.0.0&site=14&' \
                  '_lg=10&page=%s' % (keyword, page_index)
            html, res = tools.get_html_by_requests(url)
            video_list_title = tools.get_tag(html, 'div', {'class': 'v-thumb'})
            video_list_url = tools.get_tag(html, 'div', {'class': 'v-meta'})
            video_list_time = tools.get_tag(html, 'div', {'class': 'v-meta-data'})

            if not video_list_title:
                break

            for info_index, video_info in enumerate(video_list_title):
                image_url = tools.get_info(str(video_info), 'src="(.+?)"', fetch_one=True)
                image_url = 'http:' + image_url
                print(image_url)
                title = tools.get_info(str(video_info), 'alt="(.+?)"', fetch_one=True)
                print(title)
                url = tools.get_info(str(video_list_url[info_index]), 'href="(.+?)"', fetch_one=True)
                url = 'http:' + url
                print(url)
                release_time = tools.get_info(str(video_list_time[info_index * 2 + 1]), 'lass="r">(.+?)<',
                                              fetch_one=True)
                release_time = get_release_time(release_time)
                print(release_time)
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
