# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 22:27:51 2024

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

# 去除包含 NaN 的行，如果你希望保留这些行以后处理可以略过这步
#df.dropna(inplace=True)

# 将DataFrame转换为二维数组
data = df.values

plt.figure(figsize=(6, 6))  # 设置画布大小，单位是英寸

# 使用imshow函数显示点阵数据，设置黑白色彩映射（cmap）
plt.imshow(data, cmap='binary', interpolation='nearest')
plt.colorbar()  # 显示颜色条，用于解释颜色的值对应关系

plt.title('Binary Matrix Visualization')  # 设置图表标题
plt.grid(False)  # 关闭网格线显示

plt.show()  # 显示图表\

    

