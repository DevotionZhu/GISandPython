
# Raster栅格对象


## 常用方法

### 打开栅格数据  
		
	Raster(inRaster) #数据类型：Raster
	
	# 例子
	r = Raster("c:/data/dem") # 绝对路径
	r = Raster("19960909.img") #相对路径，当不是ArcGIS的栅格数据时，要加上后缀

### 保存栅格数据

	rasterObj.save(path) #使用：Raster对象.save(路径字符串)

	# 例子
	r.save("c:/data/dem_1") # 绝对路径保存

### 列出工作目录下的所有栅格

	arcpy.ListRasters({wild_card},{raster_type})

	# 例子：列出工作空间中的Grid栅格名称
	import arcpy
	arcpy.env.workspace = "c:/data/DEMS"
	rasters = arcpy.ListRasters("*","GRID")
	for raster in rasters:
		print raster


|参数|说明|数据类型|
|-|-|-|
|wild_card|通配符可限制返回的结果，例如匹配前面有A的文件名("A*")|String|
|raster_type|栅格格式|String|


### 栅格转换为NumPy数组
使用例子：https://blog.csdn.net/summer_dew/article/details/78867410

转换成NumPy便于我们对像元进行操作，[详细请点我](http://resources.arcgis.com/zh-cn/help/main/10.2/index.html#//03q300000029000000)

	RasterToNumPyArray (in_raster, {lower_left_corner}, {ncols}, {nrows}, {nodata_to_value})


RasterToNumPyArray支持将多波段栅格直接转换成多维数组(ndarray)

1. 如果输入Raster实例基于多波段栅格，则会返回 ndarry，其中第一维的长度表示波段数。ndarray 将具有维度（波段、行、列）
2. 如果输入Raster实例基于单个栅格或多波段栅格中的特定波段，则会返回含维度（行、列）的二维数组。


转换时隐含规则：

1. 如果数组的定义（左下角以及行数和列数）超出 in_raster 的范围，则数组值将分配为 NoData
2. 如果 lower_left_corner 与像元角不重合，则会自动捕捉到最近像元角的左下角，该捕捉方法采用的规则与“捕捉栅格”环境设置中的规则相同。RasterToNumPy 函数内的捕捉操作不会与“捕捉栅格”环境设置相混淆；该函数只使用相同的交互


	



## 属性
|属性|说明|数据类型|属性|说明|数据类型
|-|-|-|-|-|-|
|bandCount|波段数量|Integer|pixelType|像素类型(U32:Unsigned 32 bit integers)|String|
|name|数据名称|String|spatialReference|空间参考|SpatialReference|
|path|完整路径和名称|String|catalogPath|全路径和名称的字符串|String|
|compressionType|压缩类型|String|format|数据格式|String|
|extent|栅格数据的范围|Extent|hasRAT|存在关联的属性表|Boolean|
|height|行数|Integer|width|列数|Integer|
|isInteger|数据具有整数类型|Boolean|isTemporary|数据是临时的|Boolean|
|maximum|最大值|Double|minimum|最小值|Double|
|mean|平均值|Double|standardDeviation|标准差|Double|
|uncompressedSize|磁盘大小|Double|noDataValue|在数据中NoData的值|Double|

## 操作
|操作|代码示例|说明|
|-|-|-|
|求栅格数据的坡度|Slope("dem")|参数为字符串，全路径或相对路径|
|相加|Raster('19960909.img')+Raster('19960919.img')|相加得一个Raster对象|

# 案例

|名称|说明|
|-|-|
|多个栅格文件相加|创建一个相同范围，像元值都为0的栅格文件aoi_value_0，递归相加，保存|


# 错误集合
## 运行py文件出错
运行py文件出错，没有为脚本提供授权

错误：

	Traceback (most recent call last):
	  File "G:/workspace/python/arcpy/arcgis_running/file_add.py", line 6, in <module>
	    out = Raster('19990101.img') + Raster('19990111.img')
	  File "D:\Program Files (x86)\ArcGIS\Desktop10.2\arcpy\arcpy\sa\Functions.py", line 4143, in Plus
	    in_raster_or_constant2)
	  File "D:\Program Files (x86)\ArcGIS\Desktop10.2\arcpy\arcpy\sa\Utils.py", line 47, in swapper
	    result = wrapper(*args, **kwargs)
	  File "D:\Program Files (x86)\ArcGIS\Desktop10.2\arcpy\arcpy\sa\Functions.py", line 4140, in Wrapper
	    ["Plus", in_raster_or_constant1, in_raster_or_constant2])
	RuntimeError

![这里写图片描述](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcxMDI3MTc1NDIwMzQ0)
![这里写图片描述](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcxMDI3MTc1NDQxMTYy)  

解决：  
添加授权：arcpy.CheckOutExtension("spatial")

	import arcpy
	from arcpy import env
	from arcpy.sa import *
	arcpy.CheckOutExtension("spatial")
	env.workspace = "E:/user/Desktop/date"
	out = Raster('19990101.img') + Raster('19990111.img')