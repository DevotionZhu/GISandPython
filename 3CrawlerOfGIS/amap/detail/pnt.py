# -*- coding: utf-8 -*-
# @Time    : 2019/4/8 10:25
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : get_detail_info
# @Software: PyCharm
# @Version :
# @Desc    :

import json
import arcgisscripting
import os
from Tools import coordinate_conversion
import sys

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

fp = r"D:\mycode\GISandPython\3CrawlerOfGIS\amap\data\[2019-04-08 13-29-41] pois_detail.json"
out_dir = r"D:\mycode\GISandPython\3CrawlerOfGIS\amap\data"
out_name = r"park_point_amap.shp"

save_field = [
    ["name", "TEXT", 250],
    ["tag", "TEXT", 500],
    ["address", "TEXT", 250],
    ["city_name", "TEXT", 250],
    ["x_gcj02", "TEXT", 250],
    ["y_gcj02", "TEXT", 500],
    ["classify", "TEXT", 250],
    ["area", "TEXT", 500],
    ["level", "TEXT", 250],
]

infos = []
if __name__ == '__main__':

    with open(fp, "r") as f:
        pois = json.load(f)

        noBaseCnt = 0
        for poi in pois:
            info = {
                "level" : "",
                "area" : ""
            }
            # 景区等级
            if "scenic" in poi:
                if "level" in poi["scenic"]:
                    info["level"] = poi["scenic"]["level"]
            # base信息
            if "base" not in poi:
                noBaseCnt += 1
                print(poi)
                continue
            base = poi["base"]

            info["name"] = base["name"]
            info["city_name"] = base["city_name"]
            info["tag"] = base["tag"] #标签
            info["classify"] = base["classify"] #类别
            info["x_gcj02"] = base["x"]
            info["y_gcj02"] = base["y"]
            # 取面积
            if "geodata" in base:
                geodata = base["geodata"]
                if "aoi" in geodata:
                    aois = geodata["aoi"]
                    if len(aois)>1:
                        aoi = aois[0]
                        if "area" in aoi:
                            info["area"] = aoi["area"]
                            print info["area"]
            info["address"] = base["address"]

            infos.append(info)

        f.close()

    print "没有base的条数：{}".format(noBaseCnt)
    print "【infos】{}".format(infos)
    print "【json】{}".format( json.dumps(infos) )

    print "【Step】正在保存成shp文件..."
    # 创建shp
    print "[step] 创建shp"
    gp = arcgisscripting.create()
    spat_ref = "4326"
    gp.CreateFeatureClass_management(out_dir, out_name, "POINT", "", "", "", spat_ref)
    out_path = os.path.join(out_dir, out_name)

    # 创建属性
    print "[step] 创建属性"
    fields = []
    for field in save_field:
        fields.append(field[0])
        gp.AddField_management(out_path, field[0], field[1], field_length=field[2])

    # begin
    print "[step] 开始保存POIS"
    cur = gp.InsertCursor(out_path)
    newRow = cur.newRow()

    for feature in infos:
        print "[保存] %s" % str(feature)

        pnt = gp.CreateObject("point")
        XY = (feature["x_gcj02"], feature["y_gcj02"])
        pnt.X, pnt.Y = coordinate_conversion.gcj02towgs84(float(XY[0]), float(XY[1]))
        print "\tlocation : {}".format(pnt)
        newRow.Shape = pnt

        for attr_name in feature.keys():
            if attr_name in fields:
                print "\t{} : {}".format(attr_name, feature[attr_name])
                try:
                    newRow.setValue(attr_name,
                                    feature[attr_name]
                                    )
                except:
                    newRow.setValue(attr_name, " ")
        cur.InsertRow(newRow)

    del cur, newRow


    pass