
# 介绍
Arcpy是ArcGIS给出的一种地理处理处理方式，用Python实现

在ArcGIS体系中，地理处理还有其他两种方法：

1. ArcToolbox工具箱：灵活性差，不能按自己的需求进行扩展，但可以使用模型来整合工具，以实现流程化的地理处理服务
2. ArcObject（ArcGIS Engine）：灵活性很强，但实现一个功能，往往需要自己从头开始调用接口，工作繁杂且多

而Arcpy即是以上两种的中间产物，灵活性：ArcToolbox&lt;Arcpy&lt;ArcObject
它不像ArcToolbox这么死板，也不会像ArcObject工作量大，可以轻而易举的按自己的需求实现特殊的地理处理服务，但灵活性也有限，对于个人需求或简单的企业应用是可以满足的


# 按需开发

1. 在ArcToolbox中打开相应功能的工具-->打开工具帮助
2. 结合文档看懂例子
3. 根据需求改写代码-->在ArcGIS中Python窗口测试语句
4. 编写Arcpy代码，添加输入、输出变量的语句-->测试
5. 将Arcpy代码生成自定义工具

# 系统学习
Arcpy为ArcGIS针对Python给出的地理处理功能包，可以查看其完整文档对其进行学习
专栏保持更新，分两种模式
1. 小生应用示例（格式：`[Arcpy] 名称`）
2. 系统整理 类与方法（格式：`[Arcpy] 数字-名称`）

查看文档：http://resources.arcgis.com/zh-cn/help/main/10.2/index.html#/na/000v000000v7000000/

# 使用ArcPy的方法
1. ArcGIS Desktop自带Python开发环境
![IDLE](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcwOTIyMTgyMTU3NTkw)
![例子](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcwOTIyMTgyNTMwNjE1)
2. ArcMap中Python命令行
![ArcMap中Python命令行](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcwOTIyMTkwOTU5ODk4)
3. 脚本文件  
编写python代码，修改后缀为.py，双击运行

# 相关文章
1. ArcPy开发基础：https://www.jianshu.com/p/197a11a4b5df