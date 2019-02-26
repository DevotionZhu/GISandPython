@[toc]
# Geometry类
## 从Feature获取geometry
```python
# 两种方法
geometry = feature.geometry()
geometry = feat.GetGeometryRef()
```

## 常用方法
```python
geom.GetGeometryName() #要素类型
geom.GetPointCount() #要素点个数
geom.GetX(0);geom.GetY(0);geom.GetZ(0) #获得第一个坐标点的X、Y、Z
print(geom) #打印出所有点
geom.ExportToWkt() #导出WKT
```
# 几何类型
【包】org.Geometry
【类型】ogr.wkbPoint、org.wkbLineString、org.wkbPolygon

## 获取图层的几何类型
1. `layer.GetGeomType() == ogr.wkbPolygon`
2. `layer.GetGeometryName()`

> WKB（二进制Well-KnownBinary），用于不同软件程序间进行几何要素类型转换的一种二进制表示标准。
> 因为它是二进制格式，所以人们无法直接阅读获取其表示的内容，但是熟知文本格式（Well-Known Text，WKT）可以阅读。

|几何要素类型|对应OGR常量|
|-|-|
|Point|wkbPoint|
|Multipoint|wkbMultiPoint|
|Line|wkbLineString|
|Multiline|wkbMultiLineString|
|Polygon|wkbPolygon|
|Multipolygon|wkbMultiPolygon|
|Unknown geometry type|wkbUnknown（图层如果有多种几何类型就返回wkbUnknown）|
|No geometry|wkbNone|

## 点
```python
from osgeo import ogr
point = ogr.Geometry(ogr.wkbPoint)
point.AddPoint(10,20) #向Point添加多个点，不会报错，但最终只会用最后添加的点
```

## 线
```python
from osgeo import ogr
line = ogr.Geometry(ogr.wkbLineString) # 创建
line.AddPoint(10, 20) # 添加点
line.SetPoint(1, 50, 50) # 修改点坐标
line.GetPointCount() # 得到所有点数目
line.GetX(0); line.GetY(0) # 读取0号点的坐标
```

## 多边形
```python
from osgeo ipmort ogr
# 创建环
ring = ogr.Geometry(ogr.wkbLinearRing) #创建
ring.AddPoint(10,10) #添加点
ring.CloseRings() #闭合 或 添加的最后一个点和第一个相同
# 将环添加到多边形中
polygon = ogr.Geometry(ogr.wkbPolygon)
polygon.AddGeometry(outring)
polygon.AddGeometry(inring)
ring = polygon.GetGeometryRef(0) #得到多边形内的几何对象
```