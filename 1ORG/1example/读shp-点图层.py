# coding:utf8
import sys,os
from osgeo import ogr

inshp_path = r'..\..\9data\park_point_shp\xiamen_20181128_park.shp'

if __name__ == '__main__':
    # 【驱动】
    driver = ogr.GetDriverByName('ESRI Shapefile') #查找一个特定的驱动程序，名字一定要正确
    # 【数据源】
    datasource = driver.Open(inshp_path, 0) #0只读，1可写
    if datasource is None:
        sys.exit('不能够打开{0}'.format(inshp_path))
    # 【图层】
    layer = datasource.GetLayer(0) #得到第一个图层，shp文件只有一个图层
    # 【遍历图层中的要素，并输出指定属性】
    for feature in layer:
        point = feature.geometry()
        x = point.GetX(); y = point.GetY()
        name = feature.GetField('name')
        address = feature.GetField('address')
        print "x={0} y={1} name={2} address={3}".format(x, y, name, address)
    # 【遍历图层中所有要素并输出其所有属性】
    layer.ResetReading() # 这句话不能少！重置指针
    feature = layer.GetNextFeature()
    while feature:
        feature = layer.GetNextFeature()

    del datasource
