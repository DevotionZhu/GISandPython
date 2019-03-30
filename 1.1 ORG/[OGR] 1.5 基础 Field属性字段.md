
# 字段类型常量

|字段数据类型|OGR常量|
|-|-|
|Integer|OFTInteger|
|List of integers|OFTIntegerList|
|Floating point number|OFTReal|
|List of floating point numbers|OFTRealList|
|String|OFTString|
|List of strings|OFTStringList|
|Date|OFTDate|
|Time of day|OFTTime|
|Date and time|OFTDateTime|


有一些不同的属性字段类型，但并不是每一种字段类型都支持所有的数据格式。这时候用于描述各种数据格式的在线文档就派上用场了。

# 为Layer新建属性字段
【背景】要将一个字段添加到图层中，需要一个包含字段名称、数据类型、字段和精度等重要信息的FieldDefn对象（字段数据类型如上面的表）

```python
# 创建并添加第一个属性字段
coord_fld = ogr.FieldDefn('X', ogr.OFTReal)
# 设置限制
coord_fld.SetWidth(8) 
coord_fld.SetPrecision(3)
out_lyr.CreateField(coord_fld)
# 重用FieldDefn对象来创建第二个字段
coor_fld.SetName('Y')
out_lyr.CreateField(coord_fld)
```



# 更改属性定义

【函数】`AlterFieldDefn(iField, field_def, nFlags)` 
【作用】用新字段的规则替换现有的字段
【参数说明】
1. iField是想改变的属性字段对应的索引值
2. field_def是新属性字段的定义对象
3. nFlags是一个整数，是下表中的一个或多个常数的总和

【用于指明字段定义的哪个属性可以更改的标记，如果想使用多个，一起添加即可】

|需要更改的字段属性|OGR常量|
|-|-|
|Field name only|ALTER_NAME_FLAG|
|Field type only|ALTER_TYPE_FLAG|
|Field width and/or precision only|ALTER_WIDTH_PRECISION_FLAG|
|All of the above|ALTER_ALL_FLAG|

【举例】

```
# 【例子一】 更改原字段的名字
index = layer.GetLayerDefn().GetFieldIndex('NAME') #获取字段的索引值
fld_defn = ogr.FieldDefn('City_Name', ogr.OFTString) #创建新属性的字段定义
layer.AlterFieldDefn(index, fld_defn, ogr.ALTER_NAME_FLAG) 

# 【例子二】 更改字段的多个属性，例如名称和精度
lyr_defn = layer.GetLayerDefn()
index = lyr_defn.GetFieldIndex('X')
width = lyr_defn.GetFieldDefn(index).GetWidth()
fld_defn = ogr.FieldDefn('X_coord', ogr.OFTReal)
fld_defn.SetWidth(width)
fld_defn.SetPrecision(4)
flag = ogr.ALTER_NAME_FLAG + ogr.ALTER_WIDTH_PRECISION_FLAG
layer.AlterFieldDefn(index, fld_defn, flag)
	"""【注意】在此例子中创建新的字段定义时使用的是原始字段宽度
	如果没有为原始数据设置足够大的字段宽度，结果将不正确
	为了解决这个问题，需要使用与原始数据一样的字段宽度
	为了使更改的精度生效，所有记录必须重写
	为数据设置一个比它自身更高的精度并不会提高精度，因为数据不能凭空产生，但如果设置的精度不够高，精度就会降低
	"""
```



# 经验
1. 没能为GeoJSON文件设置一个精度
2. 想在shapefile中设置字段精度，必须设置字段宽度
3. 设置字段的默认值：`FieldDefn.SetDefault("我是默认值")`