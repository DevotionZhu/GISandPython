@[toc]



# 创建Feature并将要素添加到Layer
> 往现有图层中添加新要素和往全新的图层中添加要素的操作一样

【步骤】
1. 基于图层字段创建一个空要素，填充它
2. 然后把它插入到该图层

## 属性数据
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
## 点状数据集
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

## 线状数据集
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

## 多边形数据集
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

# 获取Layer中的feature
```python
# 1. 【获得图层中的要素】
feature = layer.GetFeature(0) 
# 2. 【获取图层中所有要素】
feat = layer.GetNextFeature()
while feat:
	feat = layer.GetNextFeature()
layer.ResetReading()
```
# 更新要素
> 要素更新操作也大同小异，只不过你操作的是图层中的现有要素，而不是一个空白的对象

【步骤】
1. 找到要编辑的要素，进行所需要的更改
2. 然后通过传递更改信息给SetFeature函数，而不是CreateFeature函数，来更新图层中的要素


【例子】为图层中的每一个要素添加一个唯一的ID
```python
layer.CreateField( # 添加一个ID字段
	ogr.FieldDefn('ID', ogr.OFTInteger)
) 
n = 1
for feat in layer:
	feat.SetField('ID', n) #设置字段的值
	layer.SetFeature(feat) #将数值传递给SetFeature函数，来更新图层中的要素信息
	n += 1
```

# 删除要素
> 删除要素更容易，需要知道的就是待删除要素的FID

【例子】删除字段City_Name为"Seattle"的要素
```python
# 找到目标的FID进行删除
for feat in layer:
	if feat.GetField('City_Name')=='Seattle':
		layer.DeleteFeature(feat.GetFID() ) #删除操作

"""
【但是】
1. 某些特定的数据格式使用此方式并不能完全删除要素。
2. 你可能看不出，有时要素只是被标记为删除了，而不是被完全抛出，它仍然还潜伏着。
3. 正因如此，你不会看到其他要素被分配到刚才删除的FID
4. 这意味着，如果已经删除了很多要素，在文件中可能存在大量不必要的已用空间
【所以】删除这些要素可以回收对应的空间
【如何回收对应空间】如果你有一些关系数据库的经验，应该熟悉这一点。它类似于在微软的Access数据库上运行压缩和修复或在PostgreSQL数据库中使用重组功能（VACUUM）
【具体做法】打开数据源，然后执行一条SQL语句来压缩数据库（不同的数据格式回收的方法不同）
"""
ds.ExecuteSQL('REPACK' + layer.GetName() ) #shapefile格式回收方式
ds.ExecuteSQL('RECOMPUTE EXTENT ON' + layer.GetName() ) #确保空间范围更新
	# 当现有要素发生改变或被删除后，它不会更新元数据中的空间范围
```

# 读取属性
```python
feature.GetFieldCount() # 属性总数
feature.keys() # 属性名
feat.GetField('AREA') # 获取字段
feature.GetFieldAsString("FID") # 获取字段成string
```

# 其他常用方法
```python
feature.Destory() #关闭
```

# 举例
```python
#【遍历所有属性值】
for i in range(feature.GetFieldCount() ):
	print( feature.GetField(i) )
### 【查看表的结构，各个字段的名称等信息】在layer附加信息中看
layerdef = layer.GetLayerDefn()
for i in range(layerdef.GetFieldCount() ):
	defn = layerdef.GetFieldDefn(i)
	print(defn.GetName(), defn.GetWidth(), defn.GetType(), defn.GetPrecision() )
```



