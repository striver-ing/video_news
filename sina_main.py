# -*- coding: utf-8 -*-
'''
Created on 2017-12-21 10:14
---------
@summary:
---------
@author: Boris
'''


import base.base_parser as base_parser
from base.spider import Spider
from parsers import *
from utils.log import log
from base.keywords import Keywords
import task_status
import time

tab_list = ['video_urls', 'video_site_info']  # 配置表(第一个须为url表)
tab_unique_key_list = ['url', 'site_id']  # 唯一索引
tab_ensure_index_list = [['depth', 'status'], ['read_status']]  # 配置索引(加快查找速度)
parser_list = [sina]
parser_siteid_list = []  # 对应parser的site_id
for parser in parser_list:
    site_id = parser.SITE_ID
    parser_siteid_list.append(site_id)

SLEEP_TIME =  60*60
def main():
    while True:
        if task_status.is_doing:#done
            log.debug('is doing sleep ...%ss'%SLEEP_TIME)
            time.sleep(SLEEP_TIME)
            continue

        task_status.is_doing = True

        keywords = Keywords().get_keywords()

        def begin_callback():
            log.info('\n********** spider_main begin **********')

        def end_callback():
            log.info('\n********** spider_main end **********')
            task_status.is_doing = False

        # 配置spider
        spider = Spider(tab_list, tab_unique_key_list, tab_ensure_index_list, parser_count=1,
                        site_parsers=parser_siteid_list, begin_callback=begin_callback, end_callback=end_callback,
                        parser_params=keywords)

        # 添加parser
        for parser in parser_list:
            spider.add_parser(parser)

        spider.start()


if __name__ == '__main__':
    main()
