>Python代码可以制作成ArcGIS自定义工具（脚本工具）
>该篇记录在Python代码中，如何从脚本工具得到参数。如何向脚本工具输出参数

# 设置脚本工具参数
http://resources.arcgis.com/zh-CN/help/main/10.2/index.html#/na/00150000000n000000/

# Python中获取与输出参数

# 输入
## 使用Sys
调用sys中获得参数，其下标从1开始

```python
import sys
# 参数从下标1开始
param1 = sys.argv[1]
param2 = sys.argv[2]
```


例子：https://blog.csdn.net/summer_dew/article/details/78845119

## 使用arcpy函数

```python
import arcpy
# 从下标0开始
inputShpFile = arcpy.GetParameterAsText(0)  
selectSQL = arcpy.GetParameterAsText(1) 
```

# 输出


## SetParameter
将Python参数传到脚本工具

SetParameter (index, value)
1. index 参数列表中指定参数的索引位置 Integer 
2. value 将设置指定参数属性的对象 Object 


例子：
```python
import arcpy
fc = arcpy.GetParameterAsText(0)
SR = arcpy.Describe(fc).spatialReference
arcpy.SetParameter(1, SR)
```

## 



ArcGIS Server注册文件夹：https://blog.csdn.net/me_dispose/article/details/50749050