> Python代码可以制作成ArcGIS的Toolsbox（脚本工具）
>1. 如何从脚本工具得到参数
>2. 如何向脚本工具输出参数

【步骤】
1. 编写Python代码
2. [将Python代码制作成ArcGIS的工具](http://resources.arcgis.com/zh-CN/help/main/10.2/index.html#/na/00150000001r000000/)
3. 与ArcGIS工具箱一样运行


# Python代码

## 输入
> 在最后Python代码会制作成ArcGIS的工具，那么怎么获取用户在工具箱里输入的参数呢？
> 有两种方法：
>   1. 使用sys
>   2. 使用arcpy.GetParameterAsText(0)  

【方法一】sys
调用sys中获得参数，其下标从1开始

```python
import sys
# 参数从下标1开始
param1 = sys.argv[1]
param2 = sys.argv[2]
```

例子：https://blog.csdn.net/summer_dew/article/details/78845119

【方法二】arcpy函数

```python
import arcpy
# 从下标0开始
inputShpFile = arcpy.GetParameterAsText(0)  
selectSQL = arcpy.GetParameterAsText(1) 
```

## 输出


【SetParameter】将Python参数传到脚本工具

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

## 总结
【总结】使用到的相关函数
```python
sys.argv[1] #从工具中获取用户输入的参数（下标从1开始）
arcpy.GetParameterAsText(0) #  从工具中获取用户输入的参数（下标从0开始）

arcpy.AddMessage("反馈信息") # 在运行途中，往工具箱输出相关提示信息

```


# 制作成自定义工具

【例子】
- https://blog.csdn.net/summer_dew/article/details/80713666
- https://blog.csdn.net/summer_dew/article/details/78072870