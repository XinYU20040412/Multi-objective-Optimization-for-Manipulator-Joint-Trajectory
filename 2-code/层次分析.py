# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 15:57:50 2024

@author: ASUS
"""

import numpy as np
from numpy import linalg
# np.set_printoptions(precision=4)
'''算术平均法权重'''
def arithmetic_mean(a):
    n = len(a)
    b = sum(a)
    #print('b:', b)
    # 归一化处理
    normal_a = a/b
    #print("算术平均法权重-归一化处理：")
    #print(normal_a)
    average_weight = []
    for i in range(n):
        s = sum(normal_a[i])
        #print("第{}行求和 ".format(i+1), s)
        # 平均权重
        average_weight.append(s/n)
    # print(average_weight)
    print('算术平均法权重:',np.array(average_weight))
    
    return np.array(average_weight)



'''几何平均法求权重'''
def geometric_mean(a):
    n = len(a)
    # 1表示按照行相乘，得到一个新的列向量
    b = np.prod(a, 1)
    #print(b)
    c = pow(b, 1/n)
    #print(c)
    # 归一化处理
    average_weight = c/sum(c)
    print('几何平均法权重:',average_weight)
    return average_weight


'''特征值法求权重'''
def eigenvalue(a):
    w, v = np.linalg.eig(a)
    #for i in range(len(w)):
        #print('特征值', a[i], '特征向量', v[:, i])
    index = np.argmax(w)
    w_max = np.real(w[index])
    vector = v[:, index]
    vector_final = np.transpose(np.real(vector))
    print('最大特征值:', w_max, 'CR:', (w_max-3)/2)
    normalized_weight = vector_final/sum(vector_final)
    print('特征值法归一化处理后:', normalized_weight)
    return w_max, normalized_weight


'''综合平均权重'''
def average_Weight(a):
    am = arithmetic_mean(a)
    gm = geometric_mean(a)
    ev = eigenvalue(a)[1]
    aw = np.array([am, gm, ev])
    #print(aw)
    final_weight = sum(aw)/3
    #print(final_weight)
    return final_weight


a=np.array([[1,5,7],
            [1/5,1,5],
            [1/7,1/5,1]])
print('综合三者权重为',average_Weight(a))