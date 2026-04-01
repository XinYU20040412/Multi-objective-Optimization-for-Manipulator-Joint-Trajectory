# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 09:35:48 2024

@author: ASUS
"""

import numpy as  np
from math import cos,sin,pi,acos,atan,sqrt
#初始化种群
def initialize_population(pop_size, num_params):
    return np.random.rand(pop_size, num_params)


#根据已有的三个参数寻找最终的末位置
def endpoint(x):
    a1=(320*x[0]-160)*pi/180#反归一化并且变成弧度制
    a2=(165*x[1]-60)*pi/180
    a3=(280*x[2]-200)*pi/180
    l1=300
    R2_1=np.array([[cos(a1),0,sin(a1),l1*cos(a1)],
                  [sin(a1),0,-cos(a1),l1*sin(a1)],
                  [0,1,0,600],
                  [0,0,0,1]])
    l2=1200
    R3_2=np.array([[cos(a2),-sin(a2),0,l2*cos(a2+pi/2)],
                  [sin(a2),cos(a2),0,l2*sin(a2+pi/2)],
                  [0,0,1,0],
                  [0,0,0,1]])
    l3_4=1500
    X=np.array([l3_4*cos(pi/2+a3),l3_4*sin(pi/2+a3),0,1])
    R=R2_1@R3_2
    y=np.dot(R,X)
    return y
#输出目标点在坐标系四中的坐标,为了求解关节4,5,6转角
def spacechange(x):
    a1=(320*x[0]-160)*pi/180
    a2=(165*x[1]-60)*pi/180
    a3=(280*x[2]-200)*pi/180
    l1=300
    R2_1=np.array([[cos(a1),0,sin(a1),l1*cos(a1)],
                  [sin(a1),0,-cos(a1),l1*sin(a1)],
                  [0,1,0,600],
                  [0,0,0,1]])
    l2=1200
    R3_2=np.array([[cos(a2),-sin(a2),0,l2*cos(a2+pi/2)],
                  [sin(a2),cos(a2),0,l2*sin(a2+pi/2)],
                  [0,0,1,0],
                  [0,0,0,1]])
    l3_4=1500
    R4_3=np.array([[0,cos(a3),cos(pi/2+a3),l3_4*cos(pi/2+a3)],
                   [0,sin(a3),sin(pi/2+a3),sin(pi/2+a3)*l3_4],
                   [1,0,0,0],
                   [0,0,0,1]])
    X=np.array([1500,1200,200,1])
    R=R2_1@R3_2@R4_3
    # 计算A的逆矩阵
    R_inv = np.linalg.inv(R)
    y=np.dot(R_inv, X)
    return y
#输出后三位参数优化调控方向,输入前三个参数角度值
def lastthere(x):
    P=spacechange(x)
    x0=P[0]
    y0=P[1]
    z0=P[2]
    cos=x0/sqrt(x0**2+y0**2)
    a=acos(cos)
    tan=z0/sqrt(x0**2+y0**2)
    b=atan(tan)
    a4=a-2*pi
    a5=0
    a6=pi/2-b
    l=[a4,a5,a6]
    return l
def RMSE(x):#定义适应度（即欧氏距离）
    P=endpoint(x)
    x0=P[0]
    y0=P[1]
    z0=P[2]
    RMSE=(1500-x0)**2+(1200-y0)**2+(200-z0)**2
    return sqrt(RMSE)#应该会在选择的时候出问题，要改适应度


# 选择操作：轮盘赌选择
def selection(population, fitness_scores):
    # 使用轮盘赌选择父代
    probabilities = fitness_scores / np.sum(fitness_scores)
    parent_indices = np.random.choice(len(population), size=len(population), replace=True, p=probabilities)
    return population[parent_indices]
# 交叉操作：单点交叉
def crossover(parents, parent_indices):
    parent1_idx, parent2_idx = parent_indices
    parent1 = parents[parent1_idx]
    parent2 = parents[parent2_idx]
    
    crossover_point = np.random.randint(1, len(parent1))
    child1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
    child2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])
    return child1, child2
# 变异操作：简单位变异
def mutate(child):
    mutation_point = np.random.randint(0, len(child))
    child[mutation_point] = np.random.rand()
    return child

# 遗传算法
def genetic_algorithm(num_generations, pop_size, num_params):
    population = initialize_population(pop_size, num_params)
    
    for generation in range(num_generations):
        RMSE_scores = np.array([RMSE(x) for x in population])
        parents = selection(population, RMSE_scores)
        next_population = []
        
        while len(next_population) < pop_size:
            parent_indices = np.random.choice(len(parents), size=2, replace=False)
            child1, child2 = crossover(parents, parent_indices)
            child1 = mutate(child1)
            child2 = mutate(child2)
            next_population.extend([child1, child2])
        
        population = np.array(next_population[:pop_size])  # 截取前pop_size个体作为下一代种群
    
    # 计算最终种群的适应度值
    RMSE_scores = np.array([RMSE(x) for x in population])
    best_individual = population[np.argmin(RMSE_scores)]
    best_fitness = RMSE(best_individual)
    
    return best_individual, best_fitness

# 示例运行
best_individual, best_fitness = genetic_algorithm(num_generations=100, pop_size=200, num_params=3)
print("Best individual:", best_individual)
print("Best fitness:", best_fitness)

t=lastthere(best_individual)
tt=np.array(best_individual)
theta=np.append(tt, t)
print(theta)#输出最终的六个调控角度


import scipy.integrate as spi



'''求解能耗
theta0=[0,-pi/2,0,pi,-pi/2,0]
w_mean=[2.0,1.5,1.0,2.5,3.0,2.0]
I=[0.5,0.3,0.4,0.6,0.2,0.4]
def e_cost(x):
    l=[]
    for i in range(0,len(x)):
        theta_f=x[i]+theta0[i]
        w0=w_mean[i]
        I0=I[i]
        t=abs(x[i])*180/(pi*w0)
        xita=np.array([theta0[i],theta_f,0,0])
        Rt=np.array([[1,0,0,0],
                     [1,t,t**2,t**3],
                     [0,1,0,0],
                     [0,1,2*t,3*t**2]])
        Rt_inv= np.linalg.inv(Rt)
        aa=np.dot(Rt_inv,xita)
        def omega_2(t):
            return (aa[1]+2*aa[2]*t+3*aa[3]*t**2)**2
        time=np.linspace(0,t,1000)
        # 使用 quad 函数进行数值积分
        result, error = spi.quad(omega_2, 0, t)  # 积分函数，积分下限，积分上限
        r=result*0.5*I0/t
        l.append(r)
    return l
print('六个关节能耗为：',e_cost(theta))


'''


theta0 = [0, -pi/2, 0, pi, -pi/2, 0]
w_mean = [2.0, 1.5, 1.0, 2.5, 3.0, 2.0]
I = [0.5, 0.3, 0.4, 0.6, 0.2, 0.4]

def e_cost(theta):
    l = []
    for i in range(len(theta)):
        if i!=4:
            theta_f = theta[i] + theta0[i]
            w0 = w_mean[i]
            I0 = I[i]
            t = abs(theta[i]) * 180 / (pi * w0)
            
            xita = np.array([theta0[i], theta_f, 0, 0])
            Rt = np.array([[1, 0, 0, 0],
                           [1, t, t**2, t**3],
                           [0, 1, 0, 0],
                           [0, 1, 2*t, 3*t**2]])
            
            # 使用 numpy.linalg.solve 求解线性方程组，代替求逆
            aa = np.linalg.solve(Rt, xita)
            
            def omega_2(t):
                return (aa[1] + 2 * aa[2] * t + 3 * aa[3] * t**2) ** 2
            
            # 调整积分函数的定义域和精度
            time = np.linspace(0, t, 1000)
            result, error = spi.quad(omega_2, 0, t, epsabs=1.0e-6, epsrel=1.0e-6)  # 增加积分精度
            
            r = result * 0.5 * I0 / t
            l.append(r)
        else:
            l.append(0)
            
        
    return l


print('六个关节能耗为：', e_cost(theta))


        
        
        
        






