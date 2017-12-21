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

SITE_ID = 1712200005
NAME = '搜狐'


def get_release_time(release_time):
    try:
        data = tools.time.time()
        ltime = tools.time.localtime(data)
        timeStr = tools.time.strftime("%Y-%m-%d", ltime)
        if '天前' in release_time:
            ndays = tools.re.compile('(\d+)天前').findall(release_time)
            days_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(days=int(ndays[0])))
            release_time = days_ago.strftime("%Y-%m-%d")
        elif '小时前' in release_time:
            nhours = tools.re.compile('(\d+)小时前').findall(release_time)
            hours_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(hours=int(nhours[0])))
            release_time = hours_ago.strftime("%Y-%m-%d %H:%M")
        elif tools.re.compile('分钟前').findall(release_time):
            nminutes = tools.re.compile('(\d+)分钟前').findall(release_time)
            minutes_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(minutes=int(nminutes[0])))
            release_time = minutes_ago.strftime("%Y-%m-%d %H:%M")
        else:
            if len(release_time) < 10:
                release_time = '%s-%s' % (timeStr[0:4], release_time)
    except:
        release_time = ''
    finally:
        return release_time


# 必须定义 添加网站信息
@tools.run_safe_model(__name__)
def add_site_info():
    log.debug('添加网站信息')

    table = 'VIDEO_NEWS_site_info'
    url = 'https://tv.sohu.com/'

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
            url = 'https://so.tv.sohu.com/mts?wd=%s&c=0&v=0&length=0&limit=0&site=0&o=3&p=%s&st=&suged=&filter=0' % \
                  (keyword, page_index)
            html, res = tools.get_html_by_requests(url)
            video_list_time = tools.get_tag(html, 'a', {'class': 'tcount'})
            video_list_title = tools.get_tag(html, 'div', {'class': 'pic170'})

            if not video_list_title:
                break
            for info_index, video_info in enumerate(video_list_title):
                image_url = tools.get_tag(video_info, 'img', find_all=False)['src']
                image_url = 'http:' + image_url
                title = video_info.a['title']
                url = video_info.a['href']
                url = 'http:' + url
                release_time = video_list_time[info_index].get_text()
                release_time = get_release_time(release_time)
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
