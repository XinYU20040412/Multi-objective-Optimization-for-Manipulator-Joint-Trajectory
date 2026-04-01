# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 02:47:22 2024

@author: ASUS
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = r"C:\Users\ASUS\Desktop\数学建模\华数杯\A题\A题\附件.xlsx"

# 读取 Excel 文件
df = pd.read_excel(file_path, sheet_name='Sheet2')

# 将数据类型尝试转换为整数，遇到无法转换的地方用 NaN 替代
df = df.apply(pd.to_numeric, errors='coerce')

# 获取原始数据的二维数组
data = df.values

# 创建一个与 data 相同形状的数组，用于标记非数值数据的位置
non_numeric_mask = np.isnan(data)

# 将非数值部分设置为一个特定值（例如 -999），在图像中显示为明显的颜色
data[non_numeric_mask] = 0.5

plt.figure(figsize=(6, 6))  # 设置画布大小，单位是英寸

# 使用imshow函数显示点阵数据，设置黑白色彩映射（cmap），但标记非数值数据的位置为特定颜色
plt.imshow(data, cmap='binary', interpolation='nearest', 
           vmin=np.nanmin(data), vmax=np.nanmax(data))
plt.colorbar()  # 显示颜色条，用于解释颜色的值对应关系

plt.title('Binary Matrix Visualization')  # 设置图表标题
plt.grid(True)  # 关闭网格线显示

plt.show()  # 显示图表
