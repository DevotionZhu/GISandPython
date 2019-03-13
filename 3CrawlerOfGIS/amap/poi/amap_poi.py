# coding:utf-8
# @Author:PasserQi
# @Time:2019/03/08
# @Desc:
#   [高德地图API] https://lbs.amap.com/api/webservice/guide/api/search
import urllib
import json
import os
from Tools import coordinate_conversion
from Tools import crawler_log
import arcgisscripting

from amap.poi import config

def get_pois():
    """ 获取pois
    API文档： https://lbs.amap.com/api/webservice/guide/api/search
    :return: pois list
    """
    print "【Step】正在获取POI..."
    pois = []
    for page in range(1, config.MAX_PAGE) : #页
        config.url_param["page"] = page
        print "当前 %s 页..." % page
        params = urllib.urlencode(config.url_param)
        # 【例如】http://restapi.amap.com/v3/place/text?city=%E5%8E%A6%E9%97%A8&citylimit=true&key=4fac3db866dcc3b8a735651d3a7db1c7&offset=20&output=json&page=1&types=%E5%85%AC%E5%9B%AD
        url = "http://restapi.amap.com/v3/place/text?%s" % params
        print "\t[url] %s" % url
        line = urllib.urlopen(url).readline()
        obj = json.loads(line)
        if "pois" not in obj:
            print "该请求没有pois"
            continue
        pois_tmp = obj["pois"]
        if len(pois_tmp)!=0:
            # 加到返回值
            for poi in pois_tmp:
                poi["poiid"] = poi["id"]
                pois.append(poi)
        else: # 已经没有POI了，不需继续请求下一页
            break
    crawler_log.save_json(pois, config.out_dir, "pois")
    return pois

def save_pois(pois):
    print "【Step】正在保存成shp文件..."
    # 创建shp
    gp = arcgisscripting.create()
    spat_ref = "4326"
    gp.CreateFeatureClass_management(config.out_dir, config.out_name, "POINT", "", "", "", spat_ref)
    out_path = os.path.join(config.out_dir, config.out_name)

    # 创建属性
    fields = []
    for field in config.save_field:
        fields.append(field[0])
        gp.AddField_management(out_path, field[0], field[1], field_length=field[2])

    # begin
    cur = gp.InsertCursor(out_path)
    newRow = cur.newRow()

    for feature in pois:
        for attr_name in feature.keys():
            if attr_name == "location":
                pnt = gp.CreateObject("point")
                XY = feature[attr_name].split(",")
                pnt.X, pnt.Y = coordinate_conversion.gcj02towgs84(float(XY[0]), float(XY[1]))
                newRow.Shape = pnt
                continue
            if attr_name in fields:
                newRow.setValue(attr_name, feature[attr_name])
        cur.InsertRow(newRow)

    del cur, newRow


if __name__ == '__main__':
    # 【获得POIS】
    # pois = get_pois()
    pois = crawler_log.read_json(r'D:\mycode\GISandPython\3AMap\poi\data\pois2019-03-13 14-53-13.json')
    print pois
    # 【保存】
    save_pois(pois)

