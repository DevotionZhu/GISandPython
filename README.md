Author: [PasserQi](https://blog.csdn.net/summer_dew)


> 开源GIS与Python  
> 主题：使用Python实现GIS的相关处理  
> 内容：入门+示例+应用代码


Markdown-toc


【项目文件目录介绍】

- GISandPython
    - 0StudyMaterials #学习资料
    - 1ORG  #ORG模块的使用-矢量数据处理
    - 2GDAL #GDAL模块的使用-栅格数据处理
    - 3Proj.4 #开源的地图投影库
    - 4Mapnik #地图渲染与出图




# Python与开源GIS
【学习网站】http://pygis.osgeo.cn



## 基础类库（抽象库）
- GDAL 是大部分开源GIS的基础，也包括如ArcGIS这样的商业软件
- Proj.4 地图投影类库
- geojson类库，用于 GeoJson 格式的数据处理
- Rasterio用于栅格影像处理
- Geos是由C开发的空间关系与分析类库

## Python类库
- Shapley 是基于 Geos 的封装 Python 库
- Fiona 用于矢量数据的读入、写出
- Rtree 是Rtree空间索引的类库
- pyproj 是Proj.4的Python 接口扩展
- python-rasterstats 用于栅格数据的计算
- OWSLib 基于OGC标准进行信息访问
- basemap 基于 Matplotlib 的绘图库
- descartes 运用matplotlib对空间数据画图
- mercantile 球面墨卡托投影

## GIS工具
- GeoPandas：整合了pandas,shapely,fiona,descartes,pyproj和rtrees，用于数据处理
GeoDjango django出品，集成了GIS功能的门户网站程序
- python-rasterstats 栅格数据统计

# GDAL项目
【学习资料】
1. 官方网站：https://www.gdal.org/
2. 犹他州立大学——开源GIS类库GDAL资料：Python GDAL课程笔记：http://www.osgeo.cn/python_gdal_utah_tutorial/
2. OSGeo中国的文档：http://pygis.osgeo.cn/gdal_begin.html
3. OSGeo中国的教程：http://www.osgeo.cn/page/python_opengis
4. GDAL开发文档：https://gdal.org/python/


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
【抽象数据模型ADM】
1. GDAL使用抽象数据模型（Abstract Data Model）来解析它所支持的数据格式
2. 抽象数据模型包括数据集（Dataset）、坐标系统、仿射地理坐标转换（Affine GeoTransform）、大地控制点（GCPs）、元数据（Metadata）、栅格波段（Raster Band）、颜色表（Color Table）、子数据集域（Subdatasets Domain）、图像结构域（Image_Structure Domain）、XML域（XML：Domains）
3. 【详细结构描述】https://www.gdal.org/gdal_datamodel.html

【GDAL核心类结构】

- GDALMajorObject类：带有元数据的对象
	- GDALDataset类：
	①从一个栅格文件中提取的相关联的栅格波段集合和这些波段的元数据；
	②GDALDataset叶负责所有栅格波段的地理坐标转换和坐标系定义
	- GDALDriver类：文件格式驱动类，GDAL会为每一个所支持的文件格式创建一个该类的实体，来管理该文件格式
	- GDALDriverManger类：文件格式驱动管理类，用来管理GDALDriver类
	- GDALRasterBand类

### OGR-处理矢量数据
【支持的文件格式】shapefiles、S-57、SDTS、PostGIS、Oracle Spatial、Mapinfo mid/mif、Mapinfo TAB

【OGR体系结构】
1. Geometry：类Geometry（包括OGRGeometry等类）封装了OpenGIS的矢量数据模型，并提供了一些几何操作，WKB（Well Knows Binary）和WKT（Well know Text）格式之间的相互转换，以及控件参考系统（投影）
2. Spatial Reference类：封装了投影和基准面的定义
3. Feature：封装了一个完整的Feature的定义，一个完整的Feature包括一个Geometry和一系列属性
4. Feature Definition：类 OGRFeatureDefn 里面封装了 feature 的属性，类型、名称及其默认的空间参考系统等。一个 OGRFeatureDefn 对象通常与一个层(layer)对应。
5. Layer：类 OGRLayer 是一个抽象基类，表示数据源类 OGRDataSource 里面的一层要素(Feature)。
6. Data Source：类 OGRDataSource 是一个抽象基类，表示含有 OGRLayer 对象的一个文件或一个数据库
7. Drivers：类 OGRSFDriver 对应于每一个所支持的矢量文件格式。类OGRSFDriver 由类 OGRSFDriverRegistrar 来注册和管理。



