# 	拷贝
## datasource层次的拷贝
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

## layer层次的拷贝
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

## feature层次的拷贝
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
