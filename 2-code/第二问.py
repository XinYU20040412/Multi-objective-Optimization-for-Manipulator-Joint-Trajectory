# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 23:12:07 2024

@author: ASUS
"""

'''层次分析AHP'''
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














'''第二问优化'''
import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, pi, acos, atan, sqrt

# Constants and parameters
POP_SIZE = 200
NUM_PARAMS = 3
NUM_GENERATIONS = 100
MUTATION_RATE = 0.1
CROSSOVER_PROB = 0.8

# Initialize population
def initialize_population(pop_size, num_params):
    return np.random.rand(pop_size, num_params)

# Compute end-effector position
def endpoint(x):
    a1 = (320*x[0] - 160) * pi / 180
    a2 = (165*x[1] - 60) * pi / 180
    a3 = (280*x[2] - 200) * pi / 180
    
    l1 = 300
    R2_1 = np.array([[cos(a1), 0, sin(a1), l1*cos(a1)],
                     [sin(a1), 0, -cos(a1), l1*sin(a1)],
                     [0, 1, 0, 600],
                     [0, 0, 0, 1]])
    
    l2 = 1200
    R3_2 = np.array([[cos(a2), -sin(a2), 0, l2*cos(a2 + pi/2)],
                     [sin(a2), cos(a2), 0, l2*sin(a2 + pi/2)],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])
    
    l3_4 = 1500
    X = np.array([l3_4*cos(pi/2 + a3), l3_4*sin(pi/2 + a3), 0, 1])
    
    R = R2_1 @ R3_2
    y = np.dot(R, X)
    
    return y
#定义重力势能
def delta_Ep(x):
    a1 = (320*x[0] - 160) * pi / 180
    a2 = (165*x[1] - 60) * pi / 180
    a3 = (280*x[2] - 200) * pi / 180
    l2=1200
    l1=300
    
    R2_1 = np.array([[cos(a1), 0, sin(a1), l1*cos(a1)],
                     [sin(a1), 0, -cos(a1), l1*sin(a1)],
                     [0, 1, 0, 600],
                     [0, 0, 0, 1]])
    P3_2=np.array([l2*cos(pi/2+a2),l2*sin(pi/2+a2),0,1])
    P3=np.dot(R2_1,P3_2)
    z3=P3[2]*10**(-3)
    z4=endpoint(x)[2]*10**(-3)
    z2=0.6
    L=0.6+0.3+1.2+1.5
    M=5
    g=9.8
    Ef=(0.3/L)*z2*M*g+(1.2/L)*M*g*(z2+z3)/2+(1.5/L)*M*g*(z4+z3)/2
    E0=M*g*L/2
    return E0-Ef
    
# Fitness function (RMSE)
def RMSE(x):
    P = endpoint(x)
    target = np.array([1500, 1200, 200])
    return np.sqrt(np.sum((P[:3] - target)**2))
def fitness(x):
    return 0.7086*RMSE(x)+0.2228*delta_Ep(x)

# Tournament selection
def tournament_selection(population, fitness_scores, tournament_size=3):
    selected_parents = []
    pop_size = len(population)
    
    for _ in range(pop_size):
        tournament_indices = np.random.choice(pop_size, size=tournament_size, replace=False)
        tournament_fitness = fitness_scores[tournament_indices]
        selected_parents.append(population[tournament_indices[np.argmin(tournament_fitness)]])
        
    return np.array(selected_parents)

# Single-point crossover
def crossover(parents, crossover_prob=CROSSOVER_PROB):
    if np.random.rand() < crossover_prob:
        crossover_point = np.random.randint(1, len(parents[0]))
        child1 = np.concatenate([parents[0][:crossover_point], parents[1][crossover_point:]])
        child2 = np.concatenate([parents[1][:crossover_point], parents[0][crossover_point:]])
    else:
        child1, child2 = parents[0].copy(), parents[1].copy()
    
    return child1, child2

# Mutation
def mutate(child, mutation_rate=MUTATION_RATE):
    for i in range(len(child)):
        if np.random.rand() < mutation_rate:
            child[i] = np.random.rand()
    return child

# Genetic algorithm
def genetic_algorithm(num_generations, pop_size, num_params):
    population = initialize_population(pop_size, num_params)
    best_fitness_history = []
    
    for generation in range(num_generations):
        fitness_scores = np.array([fitness(x) for x in population])
        best_fitness = np.min(fitness_scores)
        best_individual = population[np.argmin(fitness_scores)]
        best_fitness_history.append(best_fitness)
        
        next_population = [best_individual]  # Elitism: preserve the best individual
        
        while len(next_population) < pop_size:
            parents = tournament_selection(population, fitness_scores)
            child1, child2 = crossover(parents)
            child1 = mutate(child1)
            child2 = mutate(child2)
            next_population.extend([child1, child2])
        
        population = np.array(next_population[:pop_size])
    
    # Final best individual and fitness
    final_fitness_scores = np.array([fitness(x) for x in population])
    best_individual = population[np.argmin(final_fitness_scores)]
    best_fitness = np.min(final_fitness_scores)
    # 绘制适应度变化曲线
    plt.figure(figsize=(8, 6))
    plt.plot(range(1,len(best_fitness_history)+1), best_fitness_history, marker='o', linestyle='-', color='b')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness Change in Genetic Algorithm')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return best_individual, best_fitness, best_fitness_history

# Run the genetic algorithm
best_individual, best_fitness, best_fitness_history = genetic_algorithm(NUM_GENERATIONS, POP_SIZE, NUM_PARAMS)
print("最优前三关节调控参数:", best_individual)
print("最小距离偏差（mm）:",RMSE(best_individual) )
print('最小克服重力势能做功（J）：',delta_Ep(best_individual))



'''求解后三个调控参数'''
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
print('后三个角精细朝向调控参数为：',lastthere(best_individual))

    

'''求解能耗'''
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
t=lastthere(best_individual)
tt=np.array(best_individual)
theta=np.append(tt, t)

print('六个关节能耗为：', e_cost(theta))