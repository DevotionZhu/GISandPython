# driver、datasource

## 获取需要的驱动程序
【方法一】从已有数据源中获取驱动变量
```python
ds = ogr.open(r'D:\....\...shp')
driver = ds.GetDriver()
```
【方法二】通过名称获取 `json_driver = ogr.GetDrverByName('GeoJSON')`
名称获取方式：
1. OGR网站上有介绍，通过GDAL/ORG自带的ogrinfo
2. 代码中提供的print_drivers函数来获取驱动程序的名字

## 创建数据源
【创建数据源】有了驱动程序之后，提供数据源名称来使用它创建一个空的数据源。新创建的数据源会自动打开等待写入
```python
# 创建一个功能齐全的SpatialLite数据源，而不是使用SQLite
fn = "filename"

driver = ogr.GetDriverByName("SQLite")
# 创建新的数据源时，不能覆盖现有的数据源。如果你的代码可能会覆盖现有数据，那么在创建新数据之前需要删除旧数据
if os.path.exists(fn):
	driver.DeleteDataSource(fn)
ds= driver.CreateDataSource(fn, 
	options=[ #创建选项：传递一个字符串列表（参数在OGR网站上有文档介绍）
		'SPATIALITE=yes'
	]
)
if ds is None:
	#【注意】如果数据源没有创建成功，那么CreateDataSource函数会返回为空。如果为空对象，之后使用会报AttributeError错误
	sys.exit('Could not create {0}'.formaat(json_fn ) )
```




## 关闭
```python
datasource.Destory() #关闭
del datasource # 删除datasource
	""" 删除ds变量强制关闭文件，并将所有的编辑成果写入磁盘中
	【注意】删除图层变量并不会触发这个操作，必须关闭数据源才行
	【备注】如果想保持数据源打开的话，可以通过图层对象或者数据源对象调用ds.SyncToDisk()
	【警告】为了使你的编辑写入到磁盘中，必须关闭文件或者调用SyncToDisk函数。如果没有这么做，并且在交互环境中还打开数据源，那么你会很失望地发现创建了一个空的数据集
	"""
```


## 例子
### 打开shp

```python
from osgeo import ogr
inshp_path = 'D:\mycode\GISandPython\0data\park_point_shp\xiamen_20181128_park.shp'
driver = ogr.GetDriverByName('ESRI Shapefile') #查找一个特定的驱动程序
datasource = driver.Open(inshp_path, 0) #0只读，1可写
dir( datasource) #使用Python的内省函数dir()查看所有方法
```

### 删除数据
```python
# 删除矢量数据文件
if os.path.exists(out_shp)
	driver.DeleteDataSource(out_shp)
ds2 = driver.CreateDataSource(out_shp)
```