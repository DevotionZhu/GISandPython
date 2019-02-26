@[toc]

# Python与开源GIS
【网站】http://pygis.osgeo.cn/


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


# GDAL
GDAL/ORG是非常著名的开源GIS库，GDAL是对栅格数据进行操作，而OGR是对矢量数据进行操作。它们相当于一个通用的数据访问库


## Python安装GDAL


【步骤】
1. https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal 下载gdal
2. 命令行进行安装`pip install GDAL-2.1.3-cp35-cp35m-win_amd64.whl`
3. 检查安装是否成功`from osgeo import gdal; import ogr`
