# -*- coding: utf-8 -*-
# @Time    : 2019/5/13 9:06
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : amap
# @Software: PyCharm
# @Version :
# @Desc    :
#   [poi] http://restapi.amap.com/v3/place/text?city=%E5%8E%A6%E9%97%A8&citylimit=true&key=4fac3db866dcc3b8a735651d3a7db1c7&offset=20&output=json&page=1&types=%E5%85%AC%E5%9B%AD
#   [detail] https://ditu.amap.com/detail/get/detail?id=B0FFK7QH8K

import os, sys, time, json, requests
import arcpy, arcgisscripting  #arcpy
from Tools import coordinate_conversion #坐标转换

class amap(object):
    params = {}
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    }
    poi_url = "http://restapi.amap.com/v3/place/text"
    pois = []

    detail_url = "http://ditu.amap.com/detail/get/detail"
    details = []

    def __init__(self, params_value=None):
        # python2乱码处理
        defaultencoding = 'utf-8'
        if sys.getdefaultencoding() != defaultencoding:
            reload(sys)
            sys.setdefaultencoding(defaultencoding)

        # 获取参数
        if type(params_value) is dict: # {}对象
            self.params = params_value
        elif type(params_value) is str: # json文件中获得
            with open(params_value, 'r') as fp:
                self.params = json.loads(fp)
                fp.close()

    def set_citycode(self, citycode):
        self.params["url_param"]["city"] = citycode
        self.params["out_name"] = "{}_{}.shp".format(
            self.params["url_param"]["keywords"], citycode
        )
        print "[更改的params]{}".format(self.params)


    def crawler_nation_pnt(self):
        pass

    def crawler_pnt(self):
        pois = self.get_pois()
        self.save_pnt(pois)

    def crawler_line(self):
        pois = self.get_pois()
        # pois_detail = self.get_detail(pois)
        # self.save_line(pois_detail)
        pass

    def get_pois(self):
        """ 获取pois
        API文档： https://lbs.amap.com/api/webservice/guide/api/search
        :return: pois list
        """
        print "=== 正在获取POI ==="

        pois = []
        url_params = self.params["url_param"]
        for page in range(1, params["MAX_PAGE"]):  # 页
            url_params["page"] = page
            print "= 当前%s页" % page
            r = requests.get(self.poi_url, params=url_params, headers=self.headers)
            print "[url] {}".format(r.url)
            line = r.text
            obj = json.loads(line)
            if "pois" not in obj:
                print "[error] 该请求没有pois"
                continue
            pois_tmp = obj["pois"]
            if len(pois_tmp) != 0:
                # 加到返回值
                for poi in pois_tmp:
                    poi["poiid"] = poi["id"]
                    pois.append(poi)
            else:  # 已经没有POI了，不需继续请求下一页
                break
        self.save_json(pois, params["out_dir"], "pois")
        self.pois = pois
        return pois

    def get_detail(self, pois):
        """ 得到POI具体信息
        :param pois: list
        :return: pois_detail: list
        """
        print "=== 正在获取detail ==="
        pois_detail = []
        for index, poi in enumerate(pois):
            # poi无ID
            if "id" not in poi:
                print "[error] 当前POI无ID"
                continue
            # 拼接url
            poiid = poi["id"]
            params = {
                'id': poiid
            }
            # 请求数据
            r = requests.get(self.detail_url, params=params, headers=self.headers)
            print "[url] {}".format(r.url)
            json_str = r.text
            ret = json.loads(json_str)
            if "2001" not in ret:
                print "[error] 没有获取到ID为%s的详细信息：{}".format(poiid)
                print "[返回的数据] {}".format(json_str)
            else:
                pois_detail.append(
                    ret["2001"]
                )

            time.sleep(20)
            if index % 51 == 0:
                time.sleep(120)
        self.save_json(pois_detail, params["out_dir"], "POIdetail")
        self.details = pois_detail
        return pois_detail

    def save_pnt(self, pois):
        print "=== 正在保存成shp文件（点） ==="
        # 创建shp
        print "[step] 创建shp"
        gp = arcgisscripting.create()
        spat_ref = "4326"
        gp.CreateFeatureClass_management(params["out_dir"], params["out_name"], "POINT", "", "", "", spat_ref)
        out_path = os.path.join(params["out_dir"], params["out_name"])

        # 创建属性
        print "[step] 创建属性"
        fields = []
        for field in params["save_field"]:
            fields.append(field[0])
            gp.AddField_management(out_path, field[0], field[1], field_length=field[2])

        # begin
        print "[step] 开始保存POIS"
        cur = gp.InsertCursor(out_path)
        newRow = cur.newRow()

        for feature in pois:
            print "[保存] {}".format(feature)
            for attr_name in feature.keys():
                if attr_name == "location":
                    pnt = gp.CreateObject("point")
                    XY = feature[attr_name].split(",")
                    pnt.X, pnt.Y = coordinate_conversion.gcj02towgs84(float(XY[0]), float(XY[1]))
                    print "\t[location] {}".format(pnt)
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

    def save_line(self, pois_detail):
        """ 提取出shp属性
        :param pois_detail: list
        :return:
        """
        print "=== 正在保存成shp文件（线） ==="

        # 提取feature
        feats = []
        for index, poi_detail in enumerate(pois_detail):
            # 获得坐标串
            if "spec" not in poi_detail:
                if "base" in poi_detail and "name" in poi_detail["base"]:
                    print "[error] {} 没有坐标信息".format(poi_detail["base"]["name"])
                continue
            spec = poi_detail["spec"]
            have_shp = "没有"
            for key in spec:
                feat = {}
                if key == "mining_shape":  # 有shp
                    have_shp = "有"
                    feat["shape"] = spec[key]["shape"]  # 保存shp属性
                    feat["name"] = poi_detail["base"]["name"].encode("utf8")
                    feat["type"] = poi_detail["base"]["business"].encode("utf8")
                    feats.append(feat)

                    if len(feats) % 11 == 0:
                        print "已保存{}个信息".format( len(feats) )
                    break
            print "{} ：{}".format( poi_detail["base"]["name"].encode("utf8"), have_shp)
        self.save_json(feats, params["out_dir"], "feats")

        out_path = os.path.join(params["out_dir"], params["out_name"])
        gp = arcgisscripting.create()  # GP
        spat_ref = "4326"  # 坐标系
        gp.CreateFeatureClass_management(params["out_dir"], params["out_name"], "POLYLINE", "", "", "", spat_ref)

        gp.AddField_management(out_path, "name", "TEXT", field_length=250)
        gp.AddField_management(out_path, "type", "TEXT", field_length=250)

        cur = gp.InsertCursor(out_path)
        newRow = cur.newRow()
        for feat in feats:
            for attr in feat:
                if attr == "shape":
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
                    newRow.setValue("Shape", XYarray)
                else:
                    newRow.setValue(attr, feat[attr])
            cur.InsertRow(newRow)
        del cur, newRow
        pass

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
            XY[0], XY[1] = float(XY[0]), float(XY[1])
            point = arcpy.CreateObject("point")
            point.X, point.Y = coordinate_conversion.gcj02towgs84(XY[0], XY[1])
            XYarray.add(point)
        return XYarray

    def save_json(self, obj, out_dir, fn):
        t = time.strftime('[%Y-%m-%d %H-%M-%S] ', time.localtime(time.time()))
        out_name = t + fn + ".json"
        out_path = os.path.join(out_dir, out_name)
        with open(out_path, "w+") as json_file:
            json.dump(obj, json_file, indent=4)
            json_file.close()

        pass

    def read_json(self, fpath):
        import sys
        reload(sys)
        sys.setdefaultencoding("utf-8")
        with open(fpath, 'r') as fp:
            ret = json.load(fp)
            fp.close()
        return ret

def get_citycode(fn, col_num):
    import xlrd
    ret = []
    bk = xlrd.open_workbook(fn)
    try:
        sh = bk.sheet_by_name("Sheet1")
    except:
        print "sheet1名字已经修改，不为默认值：{Sheet1}"
        return False
    nrows = sh.nrows  # 获取行数
    for i in range(1, nrows):
        ret.append(
            sh.cell_value(i, col_num)
        )
    # 去重
    ret = list( set(ret) )
    ret.remove('')
    return ret



if __name__ == '__main__':
    # 爬取点举例
    params = {
        # 输出的文件夹
        "out_dir": r"C:\Users\PasserQi\Desktop\lmyy",
        # 输出的文件名
        "out_name": "台湾妈祖庙.shp",
        # 类型 0:point 1:line 2:polygon
        "shp_type": 0,
        # 最大页数
        "MAX_PAGE": 100000,
        # url中的参数：https://lbs.amap.com/api/webservice/guide/api/search#text
        "url_param": {
            # 【keywords】与【types】至少填一种
            "keywords": "",
            # 查看Excel文件[0 POIcode.xlsx]
            "types": "150300",
            # 【可选】查询城市：城市中文、中文全拼、citycode、adcode （查看[0citycode.xlsx]）
            "city": "台湾",
            "citylimit": "true",
            "output": "json",
            "key": "4fac3db866dcc3b8a735651d3a7db1c7"
        },
        "save_field": [
            # get_pois()中把ID保存成了poiid --> 所以保存ID要写成poiid
            ["poiid", "TEXT", 250],
            ["name", "TEXT", 250],
            ["type", "TEXT", 500],
            ["typecode", "TEXT", 250],
            ["adname", "TEXT", 250],
            ["address", "TEXT", 500],
            ["pname", "TEXT", 250],
            ["cityname", "TEXT", 250],
            ["tel", "TEXT", 250]
        ]
    }
    amap = amap(params)
    amap.crawler_pnt()

    # 全国
    # amap = amap(params)
    # citycodes = get_citycode(r"D:\mycode\GISandPython\3CrawlerOfGIS\amap\0citycode.xlsx", 2)
    # for city in citycodes:
    #     print "正在爬取：{}".format(city)
    #     amap.set_citycode(city)
    #     amap.crawler_pnt()

    # 爬取线
    # params = {
    #     # 输出的文件夹
    #     "out_dir": "D:\\mycode\\GISandPython\\3CrawlerOfGIS\\amap\\2001",
    #     # 输出的文件名
    #     "out_name": "厦门市地铁线.shp",
    #     # 类型 0:point 1:line 2:polygon
    #     "shp_type": 1,
    #     # 最大页数
    #     "MAX_PAGE": 100000,
    #     # url中的参数：https://lbs.amap.com/api/webservice/guide/api/search#text
    #     "url_param": {
    #         # 【keywords】与【types】至少填一种
    #         "keywords": "地铁",
    #         # 查看Excel文件[0 POIcode.xlsx]
    #         "types": "190000",
    #         # 【可选】查询城市：城市中文、中文全拼、citycode、adcode （查看[0citycode.xlsx]）
    #         "city": "厦门市",
    #         "citylimit": "true",
    #         "output": "json",
    #         "key": "4fac3db866dcc3b8a735651d3a7db1c7"
    #     },
    #     "save_field": [
    #         # get_pois()中把ID保存成了poiid --> 所以保存ID要写成poiid
    #         ["poiid", "TEXT", 250],
    #         ["name", "TEXT", 250],
    #         ["type", "TEXT", 500],
    #         ["typecode", "TEXT", 250],
    #         ["adname", "TEXT", 250],
    #         ["address", "TEXT", 500],
    #         ["pname", "TEXT", 250],
    #         ["cityname", "TEXT", 250],
    #         ["tel", "TEXT", 250]
    #     ]
    # }
    # amap = amap(params)
    # amap.crawler_line()

    pass