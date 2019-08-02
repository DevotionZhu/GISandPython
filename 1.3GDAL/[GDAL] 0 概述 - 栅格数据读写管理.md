[toc]

[GDAL模块介绍](https://blog.csdn.net/summer_dew/article/details/86608111#GDAL_47)
【工具库】https://gdal.org/gdal_utilities.html


【GDAL的核心类结构】

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190219110250682.png)

1. GDALMajorObject类：带有元数据的对象
2. GDALDataset类：
	- 从一个栅格文件中提取的相关联的栅格波段集合和这些波段的元数据
	- GDALDdataset 也负责所有栅格波段的地理坐标转换(georeferencing transform)和坐标系定义
3. GDALDriver类：文件格式驱动类，GDAL 会为每一个所支持的文件格式创建一个该类的实体，来管理该文件格式
4. GDALDriverManager类：文件格式驱动管理类，用来管理GDALDriver类

# 导入库
```python
from osgeo import gdal # 后来的GDAL称为OSGEO的子项目，对代码进行了重新组织
	#在RFC17号文件中，实现了Python的新的名称空间osgeo，并将gdal与ogr都包含在这个名称空间之下
from osgeo.gdalconst import * #对GDAL中用到的一些常量进行绑定
	#其中gdalconst中的常量都加了前缀，力图与其他模块减少冲突
```

# 驱动

```python
driver = gdal.GetDriverByName("HFA") #得到驱动
dirver==True #判断该驱动是否得到
driver.Register()
# 【查看系统所支持的数据格式】
from osgeo import gdal
drv_count = gdal.GetDriverCount() #得到驱动总数
for idx in range(drv_count):
	driver = gdal.GetDriver(idx) #根据索引值获取驱动
	print("%10s:%s" % (driver.ShortName, driver.LongName) )
		#ShortName与栅格数据格式在GDAL中定义的编码是一致的
		#LongName可以看成是描述性的文字
```

# 读栅格数据
## 数据集dataset

```python
from osgeo import gdal
dataset = gdal.Open("data.tif")
```

【注意】栅格数据集dataset由多个数据构成的
1. 在GDAL中，每一个波段，都是一个数据集
2. 栅格数据集还可能包含有子数据集，每子数据集又可能包含有波段

【例如】
```python
>>> dataset.RasterCount # 读取Landsat影像
2 7 #由7个波段构成的Landsat遥感影像
>>> dataset.RasterCount # 读取MODIS L1B
4 0 #数据集dataset 中的栅格数目是 0
	# 实际上，MODIS L1B 的数据格式是 HDF 格式的，它的数据是以子数据集组织的，要获取其相关的数据的信息，需要继续访问其子数据集
```

## 读取影像信息

```python
# 读取遥感影像的信息
dataset.GetDescription() # 获得栅格的描述信息，不同数据集有不同的描述
dataset.RasterCount # 获得栅格数据集的波段数
dataset.RasterXSize # 栅格数据的宽度 (X 方向上的像素个数)
dataset.RasterYSize # 栅格数据的高度 (Y 方向上的像素个数)
dataset.GetGeoTransform() # 栅格数据的空间参考
	#六参数：左上角坐标，像元 X、Y 方向大小，旋转等信息。要注意，Y 方向的像元大小为负值
dataset.GetProjection() # 栅格数据的投影
```

## 读取元数据
读取元数据：`dataset.GetMetadata()`，返回一个Map对象
【key的类型有】

- TIFFTAG_DOCUMENTNAME
- TIFFTAG_IMAGEDESCRIPTION
- TIFFTAG_SOFTWARE
- TIFFTAG_DATETIME
- TIFFTAG_ARTIST
- TIFFTAG_HOSTCOMPUTER
- TIFFTAG_COPYRIGHT
- TIFFTAG_XRESOLUTION
- TIFFTAG_YRESOLUTION
- TIFFTAG_RESOLUTIONUNIT
- TIFFTAG_MINSAMPLEVALUE (read only)
- TIFFTAG_MAXSAMPLEVALUE (read only)

## 获取波段信息
band = dataset.GetRasterBand(1) #提取第一个波段：根据数值提取波段，数值从1开始，不是0！
dir(band) #查看band对象的属性、方法
band.XSize; band.YSize #波段宽高：单位像元。与dataset.RasterXSize; dataset.RasterYSize
band.GetNoDataValue() #无意义值
band.GetMaximum(); band.GetMinimum() #最大、最小值，要先调用band.ComputeRasterMinMax()计算

【波段数据类型】常量定义的包`from osgeo import gdalconst`
`band.DataType #实际数值的数据类型。返回的是一个int型数值，其是gdalconst对应的整数值`

|类型|常量|对应的整数值|
|-|-|-|
|未知或未指定类型 |gdalconst.GDT_Unknown| 0|
|8位无符整型| gdalconst.GDT_Byte |1|
|16位无符整型 |gdalconst.GDT_UInt16| 2|
|16位整型 |gdalconst.GDT_Int16| 3|
|32位无符整型| gdalconst.GDT_UInt32| 4|
|32位整型值 |gdalconst.GDT_Int32 |5|
|32位浮点型 |gdalconst.GDT_Float32| 6|
|64位浮点型 |gdalconst.GDT_Float64| 7|
|16位复数整型 |gdalconst.GDT_CInt16| 8|
|32位复数整型 |gdalconst.GDT_CInt32| 9|
|32位复数浮点型| gdalconst.GDT_CFloat32| 10|
|64位复数浮点型| gdalconst.GDT_CFloat64| 11|

## 访问数据集的数据
```python
# 读取图像数据（以二进制的形式）
dataset.ReadRaster(self, xoff, yoff, xsize, ysize, buf_xsize=None, buf_ysize=None, buf_type=None, band_list=None)
# 读取图像数据（以numpy数组形式）
dataset.ReadAsArray(self, xoff=0, yoff=0, xsize=None, ysize=None) 
```
【参数说明】
- xoff,yoff：指定想要读取的部分原点位置在整张图像中距离全图原点的位置(以像元为单位）
- xsize,ysize： 指定要读取部分图像的矩形的长和宽（以像元为单位）
- buf_xsize，buf_ysize：可以在读取出一部分图像后进行缩放。那么就用这两个参数来定义缩放后图像最终的宽和高，gdal将帮你缩放到这个大小
- buf_type：可以对读出的数据的类型进行转换（比如原图数据类型是short，你要把它们缩小成byte）
- band_list：适应多波段的情况。可以指定要读取的哪几个波段。