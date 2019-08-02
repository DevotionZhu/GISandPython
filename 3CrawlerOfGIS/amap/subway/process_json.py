# -*- coding: utf-8 -*-
# @Time    : 2019/5/13 16:44
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : process_json
# @Software: PyCharm
# @Version :
# @Desc    :
import os
import sys
import json
import arcpy, arcgisscripting
from Tools import coordinate_conversion

dir = r"D:\mycode\GISandPython\3CrawlerOfGIS\amap\subway\xiamen"
pnt_name = "厦门地铁站.shp"
line_name = u"厦门地铁线.shp"



# python2乱码处理
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

pnts = []
lines = []
def getinfo(fpath):
    with open(fpath, "r") as fp:
        obj = json.load(fp)
        if "data" not in obj:
            print "[None] {}".format(fpath)
            return False
        if "busline_list" not in obj["data"]:
            print "[None] {}".format(fpath)
            return False

        busline_list = obj["data"]["busline_list"]
        if len(busline_list)==0:
            print "[None] {}".format(fpath)
            return False
        busline = busline_list[0]
        process_line(busline)
        process_pnt(busline["stations"])
    pass

def process_line(busline):
    feat = {}
    feat["front"] = busline["front_name"]
    feat["terminal"] = busline["terminal_name"]
    feat["name"] = busline["name"]
    feat["price"] = busline["total_price"]
    feat["length"] = busline["length"]
    xs = busline["xs"]
    ys = busline["ys"]
    feat["shape"] = {
        "xs" : xs,
        "ys" : ys
    }
    lines.append(feat)
    pass

def save_line(lines):
    print "=== 正在保存线 ==="
    print "[线数据] {}".format(lines)

    out_path = os.path.join(dir, line_name)
    gp = arcgisscripting.create()  # GP
    spat_ref = "4326"  # 坐标系
    gp.CreateFeatureClass_management(dir, line_name, "POLYLINE", "", "", "", spat_ref)

    line = lines[0]
    for key in line.keys():
        if key is "shape":
            continue
        gp.AddField_management(out_path, key, "TEXT", field_length=250)

    cur = gp.InsertCursor(out_path)
    newRow = cur.newRow()
    for feat in lines:
        for attr in feat:
            if attr == "shape":
                shape = feat["shape"]
                xs = shape["xs"].split(",")
                ys = shape["ys"].split(",")
                XYarray = gp.CreateObject("array")
                for i in range(0, len(xs) ):
                    point = gp.CreateObject("point")
                    point.X, point.Y = coordinate_conversion.gcj02towgs84(float(xs[i]), float(ys[i]) )
                    XYarray.add(point)
                newRow.setValue("Shape", XYarray)
            else:
                newRow.setValue(attr, feat[attr])
        cur.InsertRow(newRow)
    del cur, newRow
    pass

def process_pnt(stations):
    for item in stations:
        feat = {}
        feat["name"] = item["name"]
        feat["poiid1"] = item["poiid1"]
        feat["poiid2"] = item["poiid2"]
        feat["start_time"] = item["start_time"]
        feat["station_id"] = item["station_id"]
        feat["end_time"] = item["end_time"]
        feat["shp"] = item["xy_coords"]
        pnts.append(feat)
    pass

def save_pnt(pnts):
    print "=== 正在保存点 ==="
    print "[点数据] {}".format(pnts)

    # 创建shp
    print "[step] 创建点shp"
    gp = arcgisscripting.create()
    spat_ref = "4326"
    gp.CreateFeatureClass_management(dir, pnt_name, "POINT", "", "", "", spat_ref)
    out_path = os.path.join(dir, pnt_name)

    # 创建属性
    print "[step] 创建属性"
    pnt = pnts[0]
    fields = []
    for key in pnt:
        if key is "shp":
            continue
        gp.AddField_management(out_path, key, "TEXT", field_length=250)
        fields.append(key)
    print " {}".format(fields)


    # begin
    print "[step] 开始保存POIS"
    cur = gp.InsertCursor(out_path)
    newRow = cur.newRow()

    for feature in pnts:
        print "[保存] {}".format(feature)
        for attr_name in feature.keys():
            if attr_name == "shp":
                pnt = gp.CreateObject("point")
                XY = feature[attr_name].split(";")
                pnt.X, pnt.Y = coordinate_conversion.gcj02towgs84(float(XY[0]), float(XY[1]))
                print "\t[shp] {}".format(pnt)
                newRow.Shape = pnt
                continue
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

if __name__ == '__main__':
    files = os.listdir(dir)
    print "[File number] {}".format(len(files) )
    for file in files:
        fpath = os.path.join(dir, file)
        getinfo(fpath)

    save_pnt(pnts) #重复的问题
    save_line(lines)