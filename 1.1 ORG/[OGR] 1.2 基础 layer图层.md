# layer
## 获取图层
1. 根据下标来获取图层：`layer = datasource.GetLayer(0)`
对于shp它只有一个图层`

## 常用方法

```python
layer.GetGeomType() #图层几何类型
n = layer.GetFeatureCount() #要素数量
extent = layer.GetExtent() #上下左右边界
readedNum = GetFeaturesRead() #已经读取多少条Feature
layer.ResetReading() #重置内部feature指针，指向FID=0的要素
layer.GetSpatialRef() #使用wkt文本表示空间参考系统的实例
layer.schema #获取FieldDefn对象列表（属性名）
```