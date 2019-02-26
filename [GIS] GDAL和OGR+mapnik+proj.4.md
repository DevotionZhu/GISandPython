@[toc]

【学习资料】
1. http://www.osgeo.cn/page/python_opengis

【Python与GIS】Python与GIS的所有包记录
https://blog.csdn.net/summer_dew/article/details/80631011#GIS_39


# GDAL项目

## 简介
GDAL项目旨于地理数据抽象模型对地理数据文件进行读写管理；而其项目下有两大类模块：GDAL和OGR
1. GDAL库为GDAL项目中对栅格数据进行操作的模块
2. OGR库为GDAL项目中对矢量数据进行操作的模块

## 详情
【GDAL项目】Geospatial Data Abstraction Library项目，是根据地理数据抽象库对地理数据文件进行读写的一个项目

【背景】GDAL项目是用地理数据抽象模型对地理数据文件的读写管理，GDAL项目中对栅格数据的读写称为GDAL模块，对矢量数据的读写称为OGR模块
【疑问】对栅格数据读写（GDAL模块）和项目名（GDAL项目）一样，都称为GDAL；而对矢量数据读写却是OGR？

1. GDAL有两层含义
① GDAL项目：指用地理数据抽象模型来对地理数据模型进行读写管理，其包含了GDAL模块和OGR模块
② GDAL模块：特指GDAL项目中对栅格数据读写的模块。
【注意】单说GDAL，是指第一个含义。而同时谈GDAL/OGR则指的是该项目所属的模块
2. 为什么模块要这样命名？
① OGR模块的全称：OGR最初用来表示开放GIS简单要素的参考实现（OpenGIS Simple Features Reference Implementation）；但由于OGR与开放GIS简单要素规范并不完全兼容，所以名字被更改了。现在它的OGR部分并不代表任何东西，只是历史延续
② GDAL模块：还未找到依据

## GDAL/OGR模块
GDAL/OGR是著名的开源GIS库，GDAL是对栅格数据进行操作，OGR是对矢量数据进行操作


【GDAL】Geospatial Data Abstraction Library，地理控件数据抽象库
1. 是一个在 X/MIT 许可协议下的开源栅格空间数据转换库。它利用抽象数据模型来表达所支持的各种文件格式
2. 它还有一系列命令行工具来进行数据转换和处理
3. 提供对多种栅格数据的支持，包括Arc/Info ASCII Grid(asc)、GeoTiff(tiff)、Erdas Imagine Images(img)、ASCII DEM(dem)等格式

【OGR】OGR 是 GDAL 项目的一个分支，功能与GDAL类似，只不过它提供对矢量数据的支持

【选择理由】

1. ESRI的 ArcGIS，Google Earth和跨平台的GRASS GIS系统都使用了GDAL/OGR库
2. 其他很多选择，大多数都是建立在GDAL基础之上的，学会了GDAL，很容易学会其他知识

### GDAL-处理栅格数据

【GDAL模块】GDAL项目下的GDAL模块，是处理栅格数据的一种开源库

【GDAL】Geospatial Data Abstraction Library提供对多种栅格数据的支持，包括Arc/Info ASCII Grid(asc)、GeoTiff(tiff)、Erdas Imagines(img)、ASCII DEM(dem)等格式

【工作原理】GDAL使用抽象数据模型（Abstract Data Model）来解析它所支持的数据格式

【抽象数据模型包括】

1. 数据集（Dataset）
2. 坐标系统
3. 仿射地理坐标转换（Affine GeoTransform）
4. 大地控制点（GCPs）
5. 元数据（Metadata）
6. 栅格波段（Raster band）
7. 颜色表（Color Table）
8. 子数据集域（Subdatasets Domain）
9. 图像结构域（Image_Structure Domain）
10. XML域（XML：Domains）

详细结构描述：https://www.gdal.org/gdal_datamodel.html

【GDAL核心类结构】

- GDALMajorObject类：带有元数据的对象
	- GDALDataset类：
	①从一个栅格文件中提取的相关联的栅格波段集合和这些波段的元数据；
	②GDALDataset叶负责所有栅格波段的地理坐标转换和坐标系定义
	- GDALDriver类：文件格式驱动类，GDAL会为每一个所支持的文件格式创建一个该类的实体，来管理该文件格式
	- GDALDriverManger类：文件格式驱动管理类，用来管理GDALDriver类
	- GDALRasterBand类

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190219110250682.png)

### OGR-处理矢量数据
#### 矢量数据格式
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

【OGR】提供对矢量数据格式的读写支持
【支持的文件格式】ESRI Shapefiles、S-57、 SDTS、PostGIS、Oracle Spatial、Mapinfo mid/mif、Mapinfo TAB

OGR支持的文件格式详情：http://gdal.org/ogr/ogr_formats.html

#### OGR体系结构
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190219153505494.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

【OGR体系结构】
1. Geometry：类Geometry（包括OGRGeometry等类）封装了OpenGIS的矢量数据模型，并提供了一些几何操作，WKB（Well Knows Binary）和WKT（Well know Text）格式之间的相互转换，以及控件参考系统（投影）
2. Spatial Reference类：封装了投影和基准面的定义
3. Feature：封装了一个完整的Feature的定义，一个完整的Feature包括一个Geometry和一系列属性
4. Feature Definition：类 OGRFeatureDefn 里面封装了 feature 的属性，类型、名称及其默认的空间参考系统等。一个 OGRFeatureDefn 对象通常与一个层(layer)对应。
5. Layer：类 OGRLayer 是一个抽象基类，表示数据源类 OGRDataSource 里面的一层要素(Feature)。
6. Data Source：类 OGRDataSource 是一个抽象基类，表示含有 OGRLayer 对象的一个文件或一个数据库
7. Drivers：类 OGRSFDriver 对应于每一个所支持的矢量文件格式。类OGRSFDriver 由类 OGRSFDriverRegistrar 来注册和管理。

#### OGR的Geometry
OGR的Geometry模型是建立在OpenGIS的简单要素数据模型之上
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190219154154318.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)


# Proj.4
【PROJ.4】开源GIS最著名的地图投影库，它专注于地图投影的表达，以及转换，许多GIS开源软件的投影都直接使用proj.4的库文件

1. 经纬度坐标与地理坐标的转换，坐标系的转换，包括基准变换等
2. 地图投影的表达方式有多重，由于采用一种非常简单明了的投影表达，proj.4比其他的投影定义简单，很容易就能看到各种地理坐标和地理投影的参数
3. 具有强大的投影转换功能

【PROJ.4】下载bin压缩包：https://proj4.org/ -->解压缩-->配置环境变量
【开发安装】开发使用pyproj `pip2 install pyproj`

# mapnik
【mapnik】功能是把数据形式的地图，包含一些地理对象，如地图、层、数据源、特征和地理几何等，通过一个样式表的定义，渲染成位图格式，用来提供 WMS 服务。其核心是一个 C++的共享库提供空间数据访问和可视化的算法和模式。
1. 强大的使用地理控件数据，创建地理的强大工具包，其核心是一个 C++ 的共享库提供空间数据访问和可视化的算法和模式，特别是包含一些地理对象，如地图、层、数据源、特征和地理几何等
2. 它提供了一些功能，可以用来设计具有良好视觉效果的地图。Mapnik会产生地图，地图对象是Mapnik的API的核心。地图对象提供了生成图像输出格式的方法（通常是PNG或者是PDF）

【应用】

1. 可以作为C++代码共享库
5. 可以用来编写Python脚本
6. 编写和处理XML配置文件

【工作机制】
7. 它使用Painter算法来决定Z轴次序，即图层按一定顺序描绘，“顶”层在其他层之上，最后描绘
8. 在每一层中，地理空间数据可视化的显示是通过一种叫做symbolizer的东西控制的。虽然在Mapnik有许多不同类型的symbolizers可以利用，但是我们这里感兴趣的是三种symbolizers。
9. 一种样式定义了图层中对象是怎么渲染的。一种样式包含了一种或多种规则，可以有选择性的限制其输出。过滤出数据源提供的对象的一个子集。例如只显示那些具有特殊属性的对象。过滤式可以选择的--对于简单的地图通常每层有一个规则，再没有其他的过滤器。每一个规则持有一个或者多个符号，这是用于在实际输出时绘制几何图形的。根据符号类和设置几何图型可以以很多种形式产生。

# 相关资料


【相关书籍的代码及数据】

1. 代码：https://github.com/cgarrard/osgeopy-code
2. 数据：https://www.manning.com/books/geoprocessing-with-python

【模块及帮助文档】

1. 相关模块：https://blog.csdn.net/summer_dew/article/details/80631011#GIS_39
1. GDAL/OGR的帮助：gdal-dev邮件列表(https://lists.osgeo.org/listinfo/gdal-dev)是一个提出问题和获得建议的好地方，可以在上面注册或查看档案
2. Python的GDAL/OGR Cookbook包含很多例子：https://pcjericks.github.io/py-gdalogr-cookbook/
3. Fiona是一个设计为读写矢量数据的模块，并且建立在OGR之上：https://fiona.readthedocs.io/en/latest/
4. Shapely是一个用于操作几何对象的有用模块：https://shapely.readthedocs.io/en/stable
5. Rasterio构建在GDAL之上，是另一个处理栅格数据的好模块：https://github.com/mapbox/rasterio

【软件】QGIS：开源的GIS软件(www.qgis.org)