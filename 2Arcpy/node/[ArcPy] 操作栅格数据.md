Raster栅格对象，是一个引用栅格数据集的变量

- 创建语法（读取栅格）  
        
      Raster(rasterPath)
      dem = Raster("c:/data/dem") #arcgis中的栅格，不需要加后缀
      img = Raster("c:/data/xiamen.img") #img图片格式需要加后缀
    参数rasterPath为栅格路径

- 保存栅格

      RasterObj.save(rasterPathAndName) # 栅格对象.save(栅格名称)
      dem.save("c:/data/dem1")

- 属性

