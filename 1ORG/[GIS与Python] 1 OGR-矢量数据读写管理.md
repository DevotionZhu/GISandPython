[toc]

# 矢量数据格式
【shapefile格式】至少需要3个二进制文件，每个文件的用途各不相同
1. 几何信息存储在【.shp】和【.shx】文件中
2. 属性信息存储在【.dbf】文件中
3. 索引或空间参考信息等数据存储在更多的文件中
4. 只有一个图层

【GeoJSON格式】广泛使用于网络地理应用中
1. 都是纯文本文件，可以使用任何文本编辑器打开查看
2. 不同于shapefile的是，一个GeoJSON只包含一个文件，所有的必要信息都存储在这个文件里

【存储在关系数据库】支持多用户访问以及各种类型的索引

1. PostGIS控件扩展运行在PostgreSQL数据库上
2. SpatiaLite控件扩展运行在SQLite数据库上
3. ESRI公司的文件地理数据库（file geodatabase）

# OGR与矢量数据

## Geometry
【包】org.Geometry
【类型】ogr.wkbPoint、org.wkbLineString、org.wkbPolygon

### 点
```python
from osgeo import ogr
point = ogr.Geometry(ogr.wkbPoint)
point.AddPoint(10,20) #向Point添加多个点，不会报错，但最终只会用最后添加的点
```

### 线
```python
from osgeo import ogr
line = ogr.Geometry(ogr.wkbLineString) # 创建
line.AddPoint(10, 20) # 添加点
line.SetPoint(1, 50, 50) # 修改点坐标
line.GetPointCount() # 得到所有点数目
line.GetX(0); line.GetY(0) # 读取0号点的坐标
```

### 多边形
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

## 读矢量数据
【OGR读取数据的简单流程】
![OGR读取数据的简单流程](https://img-blog.csdnimg.cn/2019012220132691.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

### driver、datasource
【查看OGR支持的矢量数据格式】www.gdal.org/ogr_formats.html


```python
# 【driver、datasource】打开shp
from osgeo import ogr
inshp_path = '..../data.shp'
driver = ogr.GetDriverByName('ESRI Shapefile') #查找一个特定的驱动程序
datasource = driver.Open(inshp, 0) #0只读，1可写
dir( datasource) #使用Python的内省函数dir()查看所有方法
```
### layer

```python
# 【Layer】得到图层
layer = datasource.GetLayer(0) #对于shp它只有一个图层
dir(layer) #查看所有方法
n = layer.GetFeatureCount() #要素数量
extent = layer.GetExtent() #上下左右边界
readedNum = GetFeaturesRead() #已经读取多少条Feature
```
### feature
```python
# 【Feature】要素类

## 获取要素
### 1. 【获得图层中的要素】
feature = layer.GetFeature(0) 
### 2. 【获取图层中所有要素】
feat = layer.GetNextFeature()
while feat:
	feat = layer.GetNextFeature()
layer.ResetReading()

## 要素属性
### 1. 【获取要素属性】
feat = layer.GetFeature(0)
feat.keys()
print( feat.GetField('AREA') )
### 2. 【遍历所有属性值】
for i in range(feature.GetFieldCount() ):
	print( feature.GetField(i) )
### 3. 【查看表的结构，各个字段的名称等信息】在layer附加信息中看
layerdef = layer.GetLayerDefn()
for i in range(layerdef.GetFieldCount() ):
	defn = layerdef.GetFieldDefn(i)
	print(defn.GetName(), defn.GetWidth(), defn.GetType(), defn.GetPrecision() )

## 要素形状（Geometry）
geom = feat.GetGeometryRef() #获得要素
geom.GetGeometryName() #要素类型
geom.GetPointCount() #要素点个数
geom.GetX(0);geom.GetY(0);geom.GetZ(0) #获得第一个坐标点的X、Y、Z
print(geom) #打印出所有点
geom.ExportToWkt() #导出WKT
```

### 其他
```python
# 删除矢量数据文件
if os.path.exists(out_shp)
	driver.DeleteDataSource(out_shp)
ds2 = driver.CreateDataSource(out_shp)

# 关闭
feat.Destory()
datasource.Destory()
```

## 条件查询
### 属性查询
```python
from osgeo import ogr
import os
shpfile = r'C:\tmp\data.shp'
ds = ogr.Open(shpfile)
layer = ds.GetLayer(0) #得到图层
lyr_count = layer.GetFeatureCount()
print(lyr_count) #原先的要素总数
layer.SetAttributeFilter("AREA > 800000") #属性查询条件
lyr_count = layer.GetFeatureCount() #查询过后，layer被更新
print(lyr_count) #满足条件的layer
# 将该layer保存成shp
driver = ogr.GetDriverByName("ESRI Shapefile")
extfile = r'C:\tmp\data.shp'
if os.access( extfile, os.F_OK ):
	driver.DeleteDataSource( extfile )
newds = driver.CreateDataSource(extfile)
layernew = newds.CreateLayer('rect',None,ogr.wkbPolygon)
# 遍历，复制
feat = layer.GetNextFeature()
while feat is not None:
	layernew.CreateFeature(feat)
	feat = layer.GetNextFeature()
newds.Destroy()
```

### 空间查询

### SQL查询
```python
from osgeo import ogr
driver = ogr.GetDriverByName("ESRI Shapefile")
world_shp = r'C:\tmp\test.shp'
world_ds = ogr.Open(world_shp)
world_layer = world_ds.GetLayer()
world_layer_name = world_layer.GetName()
result = world_ds.ExecuteSQL("select * from %s where prov_id = '22' order by BNDRY_ID desc" % (world_layer_name)) # ) # ExecuteSQL是基于数据集进行的，而不是图层
resultFeat = result.GetNextFeature ()
out_shp = r'C:\tmp\test\test_sql_result.shp'
create_shp_by_layer(out_shp, result) #保存结果
# 对查询结果进行遍历
while resultFeat :
    print resultFeat.GetField('BNDRY_ID')
    resultFeat = result.GetNextFeature ()
#执行下一条SQL语句之前一定要先释放
world_ds.ReleaseResultSet(result) 
```

## 	拷贝
### datasource层次的拷贝
```python
from osgeo import ogr
import os,math
inshp = "C:\tmp\test.shp"
ds = ogr.Open(inshp)
driver = ogr.GetDriverByName("ESRI Shapefile")
outputfile = 'C:\tmp\test_copy.shp'
if os.access( outputfile, os.F_OK) : #已经有该文件
	driver.DeleteDataSource(outputfile)  #删除
pt_cp = driver.CopyDataSource(ds, outputfile) #根据数据源ds创建数据，返回指针
pt_cp.Release() #释放指针，将数据写入到磁盘
```

### layer层次的拷贝
```python
from osgeo import ogr
import os,math
inshp = "C:\tmp\test.shp"
ds = ogr.Open(inshp)
driver = ogr.GetDriverByName("ESRI Shapefile")
outputfile = "C:\tmp\test_copy2.shp"
if os.access( outputfile, os.F_OK):
	driver.DeleteDataSourse( outputfile )
layer = ds.GetLayer()
newds = driver.CreateDataSource(outputfile) #首先得有数据源
pt_layer  = newds.CopyLayer(layer, 'abcd') #复制图层，返回指针
newds.Destroy() #对newds进行Destroy()操作，才能将数据写入磁盘
```

### feature层次的拷贝
```python
from osgeo import ogr
import os,math
inshp = 'C:\tmp\test.shp'
ds = ogr.Open(inshp)
driver = ogr.GetDriverByName("ESRI Shapefile")
outputfile = 'c:\tmp\test.shp'
if os.access( outputfile, os.F_OK ):
    driver.DeleteDataSource( outputfile )
newds = driver.CreateDataSource(outputfile) #按outputfile的数据源创建一个newds
layernew = newds.CreateLayer('worldcopy',None,ogr.wkbLineString) #创建一个图层
layer = ds.GetLayer() #得到原数据源的图层
extent = layer.GetExtent() #图层范围
# 遍历旧图层的所有feature，进行复制
feature = layer.GetNextFeature()
while feature is not None: 
    layernew.CreateFeature(feature)
    feature = layer.GetNextFeature()
newds.Destroy() # 包括了将数据flush到磁盘
```

## 创建几何形状
### 属性数据
```python
from osgeo import ogr
import os,math
driver = ogr.GetDriverByName("ESRI Shapefile") #shp驱动器
extfile = 'rect_field_demo.shp' #输出的shp路径
if os.access( extfile, os.F_OK ): #文件是否已存在
    driver.DeleteDataSource( extfile )

extent = [400, 1100, 300, 600] #范围
newds = driver.CreateDataSource(extfile) #按照驱动器创建数据源
layernew = newds.CreateLayer('rect',None,ogr.wkbPolygon) #创建图层
# 创建字段
fieldcnstr = ogr.FieldDefn("fd",ogr.OFTString) #创建字段(字段名，类型)
fieldcnstr.SetWidth(32) #设置宽度
layernew.CreateField(fieldcnstr) #将字段设置到layer
fieldf = ogr.FieldDefn("f",ogr.OFTReal) 
layernew.CreateField(fieldf)
# wkt格式的polygon
wkt = 'POLYGON ((%f %f,%f %f,%f %f,%f %f,%f %f))' % (extent[0],extent[3],
    extent[1],extent[3], extent[1],extent[2],
    extent[0],extent[2], extent[0],extent[3])
geom = ogr.CreateGeometryFromWkt(wkt) #根据wkt创建geometry
feat = ogr.Feature( layernew.GetLayerDefn() ) #从layer中得到feature的要求，创建一个Feature对象
feat.SetField('fd',"这里是字段的值") #设置字段值
feat.SetGeometry(geom) #设置要素的geometry属性
layernew.CreateFeature(feat) #在图层中创建该feature
newds.Destroy() #删除（包括保存）
```
### 点状数据集
```python
from osgeo import ogr
import os,math
driver = ogr.GetDriverByName("ESRI Shapefile")
extfile = 'point_demo.shp'
point_coors = [[300,450], [750, 700], [1200, 450], [750, 200], [750, 450]]
print point_coors
driver = ogr.GetDriverByName("ESRI Shapefile")
if os.access( extfile, os.F_OK ):
    driver.DeleteDataSource( extfile )
newds  = driver.CreateDataSource(extfile)
layernew = newds.CreateLayer('point',None,ogr.wkbPoint)
for aa in point_coors:
    wkt = 'POINT (' + str(aa[0]) + ' ' + str(aa[1]) + ')'
    geom = ogr.CreateGeometryFromWkt(wkt)
    feat = ogr.Feature(layernew.GetLayerDefn())
    feat.SetGeometry(geom)
    layernew.CreateFeature(feat)
newds.Destroy()
```

### 线状数据集
```python
from osgeo import ogr
import os,math
driver = ogr.GetDriverByName("ESRI Shapefile")
extfile = 'line_demo.shp'
point_coors = [300,450, 750, 700, 1200, 450, 750, 200]
print point_coors
driver = ogr.GetDriverByName("ESRI Shapefile")
if os.access( extfile, os.F_OK ):
    driver.DeleteDataSource( extfile )
newds  = driver.CreateDataSource(extfile)
layernew = newds.CreateLayer('point',None,ogr.wkbLineString)
wkt = 'LINESTRING (%f %f,%f %f,%f %f,%f %f,%f %f)' % (point_coors[0],point_coors[1],
    point_coors[2],point_coors[3], point_coors[4],point_coors[5],
    point_coors[6],point_coors[7], point_coors[0],point_coors[1])
print(wkt)
geom = ogr.CreateGeometryFromWkt(wkt)
feat = ogr.Feature(layernew.GetLayerDefn())
feat.SetGeometry(geom)
layernew.CreateFeature(feat)
newds.Destroy()
```

### 多边形数据集
```python
from osgeo import ogr
import os,math
driver = ogr.GetDriverByName("ESRI Shapefile")
extfile = 'rect_demo.shp'
if os.access( extfile, os.F_OK ):
    driver.DeleteDataSource( extfile )
extent = [400, 1100, 300, 600]
newds = driver.CreateDataSource(extfile)
layernew = newds.CreateLayer('rect',None,ogr.wkbPolygon)
width = math.fabs(extent[1]-extent[0])
height = math.fabs(extent[3]-extent[2])
tw = width/2
th = width/2
extnew = extent[0]+tw
wkt = 'POLYGON ((%f %f,%f %f,%f %f,%f %f,%f %f))' % (extent[0],extent[3],
    extent[1],extent[3], extent[1],extent[2],
    extent[0],extent[2], extent[0],extent[3])
geom = ogr.CreateGeometryFromWkt(wkt)
feat = ogr.Feature(layernew.GetLayerDefn())
feat.SetGeometry(geom)
layernew.CreateFeature(feat)
newds.Destroy()
```

# 参考文章
1. [OSGeo中国中心](http://www.osgeo.cn/)