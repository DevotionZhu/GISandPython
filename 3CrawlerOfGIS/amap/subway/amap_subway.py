# -*- coding: utf-8 -*-
# @Time    : 2019/5/13 16:01
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : amap_subway
# @Software: PyCharm
# @Version :
# @Desc    :

# [测试url]
# https://www.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=12&city=350200&geoobj=117.901118%7C24.464235%7C118.263667%7C24.618515&keywords=%E5%9C%B0%E9%93%812%E5%8F%B7%E7%BA%BF
# https://www.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=12&city=350200&geoobj=118.015094%7C24.401924%7C118.377643%7C24.571268&keywords=%E5%9C%B0%E9%93%811%E5%8F%B7%E7%BA%BF

import requests
import json

keywords_list = [
    "地铁1号线",
    "地铁2号线",
    "地铁3号线",
    "地铁4号线",
    "地铁6号线"
]
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
}
url = "https://www.amap.com/service/poiInfo"
params = {
    "query_type" : "TQUERY",
    "pagesize" : 20,
    "pagenum" : 18,
    "qii" : True,
    "cluster_state" : 5,
    "need_utd" : True,
    "utd_sceneid" :1000,
    "div" : "PC1000",
    "addr_poi_merge" : True,
    "is_classify" :True,
    "zoom" : 12,
    "city" : 350200,
    "geoobj" : "117.901118%7C24.464235%7C118.263667%7C24.618515",
    "keywords" : "地铁1号线"
}

def crawler_subway(keywords):
    params["keywords"] = keywords
    r = requests.get(url, params=params, headers=headers)
    print "[url] {}".format(r.url)
    json_str = r.text
    ret = json.loads(json_str)
    print ret


if __name__ == '__main__':
    json_list = [

    ]