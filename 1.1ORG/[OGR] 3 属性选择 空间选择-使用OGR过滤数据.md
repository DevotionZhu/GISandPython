# 属性过滤条件
【条件语句】类似SQL语句中的Where子句
【条件语句的文档】
1. www.gdal.org/ogr_sql.html
2. www.gdal.org/ogr_sql_sqlite.html

【使用】
```python
query_str = `conttinent = "South America"` #查询语句
lyr.SetAttributeFilter(query_str) # 执行
lyr.SetAttributeFileter(None) #清除属性过滤条件来获取所有要素
```

【语句示例】
```
'Population < 50000'    #数值比较，不需要引号
'Name = "Tokyo"'        #字符串比较需要引号
'Country NOT NULL' #NOT来否定条件，NULL用于指示一个空值或属性表中没有数据值
'Population BETWEEN 25000 AND 50000'            #范围
'(Population > 25000) AND (Population < 50000)' # AND
'(Population > 50000) OR (Place_type = "Country Seat")' #OR
'Type_code IN (4, 3, 7)' 
'Name LIKE "%Seattle%"' #Link语句
```

# 空间过滤条件
【使用】
```python
# Geometry过滤
lyr.SetSpatialFilter(geometry)
lyr.SetSpatialFilter(None)
# 矩形过滤
lyr.SetSpatialFilterRect(minx, miny, maxx, maxy)
```