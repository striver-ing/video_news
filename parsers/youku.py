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
        data = tools.time.time()
        ltime = tools.time.localtime(data)
        timeStr = tools.time.strftime("%Y-%m-%d", ltime)
        if '年前' in release_time:
            years = tools.re.compile('(\d+)年前').findall(release_time)
            years_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(days=int(years[0]) * 365))
            release_time = years_ago.strftime("%Y-%m-%d")

        elif '月前' in release_time:
            months = tools.re.compile('(\d+)月前').findall(release_time)
            months_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(days=int(months[0]) * 30))
            release_time = months_ago.strftime("%Y-%m-%d")

        elif '周前' in release_time:
            weeks = tools.re.compile('(\d+)周前').findall(release_time)
            weeks_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(days=int(weeks[0]) * 7))
            release_time = weeks_ago.strftime("%Y-%m-%d")

        elif '天前' in release_time:
            ndays = tools.re.compile('(\d+)天前').findall(release_time)
            days_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(days=int(ndays[0])))
            release_time = days_ago.strftime("%Y-%m-%d")

        elif '昨天' in release_time:
            days_ago = (tools.datetime.datetime.now() - tools.datetime.timedelta(days = 1))
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
    except Exception as e:
        log.error(e)
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
        quote_keyword = tools.quote(keyword)
        for page_index in range(1, 10):
            url = 'http://www.soku.com/search_video/q_%s_orderby_2_limitdate_0?spm=a2h0k.8191407.0.0&site=14&' \
                  '_lg=10&page=%s' % (quote_keyword, page_index)
            log.debug('''
                处理: %s
                url : %s'''%(keyword, url))
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
