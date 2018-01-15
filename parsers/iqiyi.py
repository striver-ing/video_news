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

SITE_ID = 1712200003
NAME = '爱奇艺'


# 必须定义 添加网站信息
@tools.run_safe_model(__name__)
def add_site_info():
    log.debug('添加网站信息')

    table = 'VIDEO_NEWS_site_info'
    url = 'http://so.iqiyi.com'

    base_parser.add_website_info(table, site_id=SITE_ID, url=url, name=NAME)


# 必须定义 添加根url
@tools.run_safe_model(__name__)
def add_root_url(keywords):
    log.debug('''
        添加根url
        parser_params : %s
        ''' % str(keywords))
    for keyword in keywords:
        print(keyword)
        next_keyword = False
        keyword = tools.quote(keyword)
        for page_index in range(1, 20):
            url = 'http://so.iqiyi.com/so/q_%s_ctg__t_0_page_%s_p_1_qc_0_rd__site__m_4_bitrate_' % (keyword, page_index)

            print(url)
            html, res = tools.get_html_by_requests(url)
            video_list_title = tools.get_tag(html, 'a', {'class': 'figure-180101'})
            video_list_time = tools.get_tag(html, 'div', {'class': 'result_info'})
            if not video_list_time:
                print('无视频列表  跳出')
                break

            for info_index, video_info in enumerate(video_list_time):
                try:
                    image_url = tools.get_info(str(video_list_title[info_index]), 'src="(.+?)"', fetch_one=True)
                    title = tools.get_info(str(video_list_title[info_index]), 'title="(.+?)"', fetch_one=True)
                    url = tools.get_info(str(video_list_title[info_index]), 'href="(.+?)"', fetch_one=True)
                    release_time = tools.get_tag(video_info, 'em', {'class': 'result_info_desc'}, find_all=False).get_text()
                    is_continue = base_parser.save_video_info(image_url=image_url, url=url, title=title, release_time=release_time,
                                                site_name=NAME)
                    if not is_continue:
                        next_keyword = True
                        break

                except Exception as e:
                    log.error(e)

            if next_keyword:
                break


# 必须定义 解析网址
def parser(url_info):
    pass
