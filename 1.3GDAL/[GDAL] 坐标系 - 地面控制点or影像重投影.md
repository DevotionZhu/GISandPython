# 地面控制点GCP
【地面控制点】
```
gdal.GCP([x], [y], [z], [pixel], [line], [info], [id])
1. x（经度）,y（纬度）和z是点在真是世界的坐标。可选，默认为0
2. pixel是具有已知坐标的像素的列偏移（照片列数）。可选，默认为0
3. line是具有已知坐标的像素的行偏移（照片行数）。可选，默认为0
4. Info和id是两个用于标识地面控制点的可选字符串。可选，默认为""
```


【例子】往影像中设置地面控制点
说明：只是设置了地面控制点，还没有进行配准
```python
import os
import shutil
from osgeo import gdal, osr

os.chdir(r'D:\osgeopy-data\Utah') #设定默认的文件夹
shutil.copy('cache_no_gcp.tif', 'cache.tif') #复制影像

ds = gdal.Open('cache.tif', gdal.GA_Update) #打开影像

# 创建S坐标系
sr = osr.SpatialReference()
sr.SetWellKnownGeogCS('WGS84')

# 创建地面控制点：经度、纬度、z，照片列数，照片行数
gcps = [
	gdal.GCP(-111.931075, 41.745836, 0, 1078, 648),
    gdal.GCP(-111.901655, 41.749269, 0, 3531, 295),
    gdal.GCP(-111.899180, 41.739882, 0, 3722, 1334),
    gdal.GCP(-111.930510, 41.728719, 0, 1102, 2548)
]

ds.SetGCPs(gcps, sr.ExportToWkt()) #添加地面控制点
ds.SetProjection(sr.ExportToWkt()) #设置投影坐标系
ds = None 
```
【例子】将地面控制点转换为地理变换
说明：用地面控制点进行配准！
```python
old_ds = gdal.Open('cache_no_gcp.tif') #旧影像
ds = old_ds.GetDriver().CreateCopy('cache2.tif', old_ds) #复制
ds.SetProjection(sr.ExportToWkt()) #设置投影
ds.SetGeoTransform(gdal.GCPsToGeoTransform(gcps)) #将地面控制点转换为地理坐标
del ds, old_ds
```



# 影像重投影
【影像重投影】对于栅格数据，需要处理栅格数据中的
