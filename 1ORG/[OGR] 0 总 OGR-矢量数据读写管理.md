@[toc]

1. OGR介绍：(https://blog.csdn.net/summer_dew/article/details/86608111#OGR_82)
2. OGR-Python帮助文档：https://gdal.org/python/
3. 【查看OGR支持的矢量数据格式】www.gdal.org/ogr_formats.html

# 设置编码
## 全局选项
```C
OSGeo.GDAL.Gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES") #支持中文
OSGeo.GDAL.Gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")
```

## 设置创建图层选项
```python
#创建图层
out_layer = ds.CreateLayer( "CommercialHousing",
    srs=in_layer.GetSpatialRef(),
    geom_type=ogr.wkbPoint,
    options  = [ 
        "ENCODING=UTF-8"
    ]
) 
```

# 读矢量数据步骤
【OGR读取数据的简单流程】
![OGR读取数据的简单流程](https://img-blog.csdnimg.cn/2019012220132691.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

1. 打开shapefile文件，并确保该操作的结果不为空
2. 从数据源中取回第一个图层
3. 查询要素
4. 删除数据源，强制关闭文件

# 参考文章
1. OSGeo中国中心：http://www.osgeo.cn/