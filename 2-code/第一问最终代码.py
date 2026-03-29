# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:53:11 2024

@author: ASUS
"""
import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, pi, acos, atan, sqrt
import seaborn as sns
sns.set()
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

# Fitness function (RMSE)
def fitness(x):
    P = endpoint(x)
    target = np.array([1500, 1200, 200])
    return np.sqrt(np.sum((P[:3] - target)**2))

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
        
        next_population = [best_individual]  # 精英主义Elitism: preserve the best individual
        
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
    
    
    # 创建图像
    plt.figure(figsize=(8, 6))
    
    # 使用Seaborn的线性回归图绘制数据
    sns.lineplot(x=range(1, len(best_fitness_history) + 1), y=best_fitness_history, marker='o', color='b')
    
    # 设置标签和标题
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness Change in Genetic Algorithm')
    
    # 显示网格
    plt.grid(True)
    
    # 调整布局
    plt.tight_layout()
    
    # 显示图像
    plt.show()

    return best_individual, best_fitness, best_fitness_history
    return best_individual, best_fitness, best_fitness_history

# Run the genetic algorithm
best_individual, best_fitness, best_fitness_history = genetic_algorithm(NUM_GENERATIONS, POP_SIZE, NUM_PARAMS)
print("最优调控参数:", best_individual)
print("最小欧氏距离:", best_fitness)

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
