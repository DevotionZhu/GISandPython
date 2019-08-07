# -*- coding:utf-8 -*-
# @Author:PasserQi
# @Function: 爬取高德地图的道路数据
# @Version: 1.0 2019/04/16
# @Desc: arcgis/python2.7
import json
import time
import urllib
import arcgisscripting
import arcpy
import os
from Tools import coordinate_conversion
from Tools import crawler_log
import sys
import requests


defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


keywords = "地铁"
out_dir = r"D:\mycode\GISandPython\3CrawlerOfGIS\amap\data"
out_name = r"subway.shp"

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
}

def _main(_type="", _out_name="", _out_dir=""):
    global type
    global out_dir
    global out_name

    if _type!="":
        type = _type
    if _out_name!="":
        out_name = "{}.shp".format(_out_name)
    if _out_dir!="":
        out_dir = _out_dir

    # 第一步：获得poi
    # 1. 代码获得
    pois = get_pois()  # 得到POI
    print "[汇报] 已经得到%d个POI" % len(pois)
    # 2. 文件获得
    # with open(r"D:\mycode\GISandPython\3CrawlerOfGIS\amap\2001\[2019-04-28 22-58-37] pois.json", "r") as fp:
    #     pois = json.load(fp)

    # 第二步：获得poi的详细信息
    # 1. 代码获得
    pois_detail = get_poi_detail(pois)
    # 2. 文件获得
    # with open(r"D:\mycode\GISandPython\3CrawlerOfGIS\amap\2001\pois_detail2019-03-12 15-10-42.json", "r") as fp:
    #     pois_detail = json.load(fp)
    print pois_detail

    # 第三步：保存features
    # 1. 代码获得features
    feats = get_pois_detail_shp(pois_detail)
    # 2. 文件获得features
    # with open( r"D:\mycode\GISandPython\3AMap\2001\feats2019-03-12 15-10-43.json", 'r') as fp:
    #     feats = json.load(fp)
    save_pois_shp(feats)

    pass


def get_pois():
    """ 获取pois
    API文档： https://lbs.amap.com/api/webservice/guide/api/search
    :return: pois list
    """

    AMAP_API_KEY = "4fac3db866dcc3b8a735651d3a7db1c7"  # 高德地图密匙
    urlParamJson = {
        'city': '厦门',
        'output': 'json',
        'key': AMAP_API_KEY,
        'types': type,
        'citylimit': 'true',  # 只返回指定城市数据
        'offset': '20'  # 每页条数
    }
    MAX_PAGE = 100  # 最大页数

    print "正在获取POI"
    pois = []
    for page in range(1, MAX_PAGE) : #页数
        urlParamJson["page"] = page
        print "当前 %s 页..." % page
        # 【例如】http://restapi.amap.com/v3/place/text?city=%E5%8E%A6%E9%97%A8&citylimit=true&key=4fac3db866dcc3b8a735651d3a7db1c7&offset=20&output=json&page=1&types=%E5%85%AC%E5%9B%AD
        url = "http://restapi.amap.com/v3/place/text"
        r = requests.get(url, params=urlParamJson, headers=headers )
        line = r.text
        obj = json.loads(line)
        if "pois" not in obj:
            print "该请求没有pois"
            continue
        pois_tmp = obj["pois"]
        if len(pois_tmp)!=0:
            # 加到返回值
            for poi in pois_tmp:
                pois.append(poi)
        else: # 已经没有POI了，不需继续请求下一页
            break
    crawler_log.save_json(pois, out_dir, "pois")
    return pois


def get_poi_detail(pois):
    """ 得到POI具体信息
    :param pois: list
    :return: pois_detail: list
    """
    pois_detail = []
    for index,poi in enumerate(pois):
        # poi无ID
        if "id" not in poi:
            print "[ERROR] 当前POI无ID"
            continue
        # 拼接url
        poiid = poi["id"]
        params = {
            'id': poiid
        }
        # 【例如】https://ditu.amap.com/detail/get/detail?id=B0FFK7QH8K
        home = "http://ditu.amap.com/detail/get/detail"
        # 请求数据
        r = requests.get(home, params=params, headers=headers)
        print "%s".format(r.url )
        json_str = r.text
        ret = json.loads(json_str)
        if "2001" not in ret:
            print "[ERROR] 没有获取到ID为%s的详细信息：{}".format(poiid)
            print "[返回的数据] %s".format(json_str)
        else:
            pois_detail.append(
                ret["2001"]
            )

        time.sleep(20)
        if index % 51 == 0:
            time.sleep(120)
    crawler_log.save_json(pois_detail, out_dir, "{}_pois_detail".format(type) )
    return pois_detail


def get_pois_detail_shp(pois_detail):
    """ 提取出shp属性
    :param pois_detail: list
    :return: feat: list
    """
    feats = []
    for index,poi_detail in enumerate(pois_detail):
        # 获得坐标串
        if "spec" not in poi_detail:
            if "base" in poi_detail and "name" in poi_detail["base"]:
                print "[INFO] %s 没有坐标信息".format( poi_detail["base"]["name"] )
            continue
        spec = poi_detail["spec"]
        have_shp = "没有"
        for key in spec:
            feat = {}
            if key == "mining_shape": # 有shp
                have_shp = "有"
                feat["shape"] = spec[key]["shape"] #保存shp属性
                feat["name"] = poi_detail["base"]["name"].encode("utf8")
                feat["type"] = poi_detail["base"]["business"].encode("utf8")
                feats.append(feat)

                if len(feats)%11==0:
                    print "已保存%d个信息" % len(feats)

                break

        print "%s ：%s" % (poi_detail["base"]["name"].encode("utf8"), have_shp )
    crawler_log.save_json(feats, out_dir, "{}_feats".format(type))
    return feats

def getXYArray(XYsStr):
    """ 通过coordinates解析出XY的数组
    :param XYsStr: 格式"x,y;x,y;x,y..."
    :desc: 传入为gcj02坐标系坐标，返回wgs84坐标
    :return: arr: 类型arcpy.array
    """
    XYarray = arcpy.CreateObject("array")
    XYList = XYsStr.split(';')
    for XYstr in XYList:
        XY = XYstr.split(',')
        XY[0],XY[1] = float(XY[0]),float(XY[1])
        point = arcpy.CreateObject("point")
        point.X,point.Y = coordinate_conversion.gcj02towgs84(XY[0], XY[1])
        XYarray.add(point)
    return XYarray

def save_pois_shp(feats):
    """ 将feats保存成shp
    :param feats: {}
    :return:
    """
    print "[Done] %d" % len(feats)
    out_path = os.path.join(out_dir, out_name)
    gp = arcgisscripting.create() #GP
    spat_ref = "4326" #坐标系
    gp.CreateFeatureClass_management(out_dir, out_name, "POLYLINE", "", "", "", spat_ref)

    gp.AddField_management(out_path, "name", "TEXT", field_length=250)
    gp.AddField_management(out_path, "type", "TEXT", field_length=250)

    cur = gp.InsertCursor(out_path)
    newRow = cur.newRow()
    for feat in feats:
        for attr in feat:
            if attr=="shape":
                # array = getXYArray(parkInfo["shape"])
                XYsStr = feat["shape"]
                XYarray = gp.CreateObject("array")
                XYList = XYsStr.split(';')
                for XYstr in XYList:
                    XY = XYstr.split(',')
                    XY[0], XY[1] = float(XY[0]), float(XY[1])
                    point = gp.CreateObject("point")
                    point.X, point.Y = coordinate_conversion.gcj02towgs84(XY[0], XY[1])
                    XYarray.add(point)
                newRow.setValue("Shape",XYarray)
            else:
                newRow.setValue(attr, feat[attr] )
        cur.InsertRow(newRow)
    del cur,newRow

if __name__ == '__main__':
    _main()