@[toc]
【学习资料】
1. http://www.osgeo.cn/page/python_opengis

【Python与GIS】Python与GIS的所有包记录
https://blog.csdn.net/summer_dew/article/details/80631011#GIS_39


# GDAL
GDAL项目旨于地理数据抽象模型对地理数据文件进行读写管理；而其项目下有两大类模块：GDAL和OGR
1. GDAL库为GDAL项目中对栅格数据进行操作的模块
2. OGR库为GDAL项目中对矢量数据进行操作的模块

详细介绍：https://blog.csdn.net/summer_dew/article/details/86600257

## GDAL-Python
GDAL库最初是C和C++编写的，但它与其他几种语言，包括Python，做了绑定，所以尽管这些代码没有用Python进行重写，但它为Python中使用GDAL/OGR库提供了接口


### GDAL-Python安装
1. https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal 下载gdal
2. 命令行进行安装`pip install GDAL-2.1.3-cp35-cp35m-win_amd64.whl`
3. 检查安装是否成功`from osgeo import gdal; import ogr`

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