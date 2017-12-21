# -*- coding: utf-8 -*-
'''
Created on 2017-01-03 11:05
---------
@summary: 提供一些操作数据库公用的方法
---------
@author: Boris
'''
import sys
sys.path.append('../../')
import init

import utils.tools as tools
from db.elastic_search import ES

es = ES()

def set_mapping():
    mapping = {
        "video_news":{
            "properties":{
                "site_name":{
                    "type":"string",
                    "index":"not_analyzed"
                },
                "summary":{
                    "type":"string",
                    "analyzer":"ik_max_word"
                },
                "time_length":{
                    "type":"long"
                },
                "play_count":{
                    "type":"long"
                },
                "comment_count":{
                    "type":"long"
                },
                "praise_count":{
                    "type":"long"
                },
                "author":{
                    "type":"string",
                    "index":"not_analyzed"
                },
                "image_url":{
                    "type":"string",
                    "index":"not_analyzed"
                },
                "domain":{
                    "type":"string",
                    "index":"not_analyzed"
                },
                "title":{
                    "type":"string",
                    "analyzer":"ik_max_word"
                },
                "record_time":{
                    "type":"date",
                    "format":"yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                },
                "uuid":{
                    "type":"string",
                    "index":"not_analyzed"
                },
                "content":{
                    "type":"string",
                    "analyzer":"ik_max_word"
                },
                "url":{
                    "type":"string",
                    "index":"not_analyzed"
                },
                "release_time":{
                    "type":"date",
                    "format":"yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                }
            }
        }
    }


    es.set_mapping('video_news', mapping)


if __name__ == '__main__':
    set_mapping()