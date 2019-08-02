# -*- coding: utf-8 -*-
# @Time    : 2019/7/3 11:48
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : geocoding
# @Software: PyCharm
# @Version :
# @Desc    :

import xlwt
import xlrd
import urllib
from bs4 import BeautifulSoup
import coordinate_conversion



NAME = u"地理编码" #输出的名称
input_path = r'C:\Users\PasserQi\Desktop\xj\20190628\xj.xlsx'
outPath = r"C:\Users\PasserQi\Desktop\xj\20190628\%s.xls" % NAME

saveField = ["查询条件","id","name","type","typecode","address","x","y","tel","pname","cityname","adname","business_area","photos"]
AMAP_API_KEY = "4fac3db866dcc3b8a735651d3a7db1c7" #高德地图密匙

# @Fun：获取查找的条件
# @Param：xls文件全路径
# @Return：[{}, {}, {}, ..] 查找的信息Items
def getItems(input_path):
    items = []
    word = xlrd.open_workbook(input_path)
    table = word.sheets()[0]
    nrows = table.nrows
    for i in range(1,nrows):
        items.append({
            "keywords" : table.cell(i,1).value,
            # "name" : table.cell(i,3).value,
            # "type" : table.cell(i,2).value
        })

    return items

# 将查找条件输出字符串
def itemToStr(item):
    ret = ""
    for key in item:
        ret += key +":" + item[key] + "\n"
    return ret


# 填写查询条件
# @param：一个查询条件
# @return：POI
def searchLocation(item):
    urlParamJson = {
        # 'city': item["name"].encode("utf8"),
        'output': 'xml',
        'key': AMAP_API_KEY,
        'keywords': item["keywords"].encode("utf8") ,
        # "types": "公司",
        'citylimit': 'true',  # 只返回指定城市数据
        'offset': '20'  # 每页条数
    }
    params = urllib.urlencode(urlParamJson)
    url = "http://restapi.amap.com/v3/place/text?%s" % params
    print url
    http = urllib.urlopen(url)
    dom = BeautifulSoup(http)
    poiList = dom.findAll("poi")
    if len(poiList) == 0:  # 没有
        return None
    else:
        return poiList[0]


if __name__ == '__main__':
    # 获取查找条件
    items = getItems(input_path)

    #创建保存的xls
    w = xlwt.Workbook(encoding="utf-8")
    #create sheet
    sheet = w.add_sheet(NAME)
    for i in range( len(saveField) ) :
        sheet.write(0, i, saveField[i])

    cur = 1
    error = 0
    # 开始查找
    for item in items:
        poi = searchLocation(item)
        index = saveField.index("查询条件")  # 获取下标
        value = itemToStr(item)
        sheet.write(cur, index, value)  # 保存
        # 没有搜索到，退出本次
        if not poi:
            cur += 1
            error +=1 # 记录未搜索到的
            continue

        # 保存
        for tag in poi:
            name = tag.name  # 标签名
            if name == "photos":  # 图片
                index = saveField.index("photos")
                value = ""
                for i in tag:
                    photos_url = tag.url.get_text()
                    value = value + photos_url + ";"
                sheet.write(cur, index, value)
                continue
            if name in saveField:
                index = saveField.index(name)  # 获取下标
                value = tag.get_text()  # 获取值
                sheet.write(cur, index, value)  # 保存
            if name == "location":
                value = tag.get_text()
                x, y = value.split(',')
                x, y = coordinate_conversion.gcj02towgs84(float(x), float(y))
                # save x
                index = saveField.index('x')
                value = x
                sheet.write(cur, index, value)
                # save y
                index = saveField.index('y')
                value = y
                sheet.write(cur, index, value)
        cur += 1
        print cur

    sheet.write(cur, 0, "失败" + str(error) )
    w.save(outPath)