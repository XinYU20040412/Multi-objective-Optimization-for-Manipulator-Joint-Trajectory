# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 22:48:05 2024

@author: ASUS
"""

import numpy as np
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = r"C:\Users\ASUS\Desktop\数学建模\华数杯\A题\A题\附件.xlsx"

# 读取 Excel 文件
df = pd.read_excel(file_path, sheet_name='Sheet1')

# 定义障碍物矩阵，0表示可通行，1表示障碍物
obstacle_matrix = df.values

class AntColonyOptimization:
    def __init__(self, obstacle_matrix):
        self.obstacle_matrix = obstacle_matrix
        self.num_ants = 10  # 蚂蚁数量
        self.max_iter = 100  # 最大迭代次数
        self.alpha = 0.1  # 信息素重要程度因子
        self.beta = 5.0  # 启发函数重要程度因子
        self.rho = 0.1  # 信息素挥发因子
        self.q = 100  # 信息素增加强度系数
        self.num_nodes = len(obstacle_matrix)  # 矩阵大小，假设是方阵

    def calculate_distance(self, path):
        distance = 0
        for i in range(len(path) - 1):
            node1 = path[i]
            node2 = path[i + 1]
            distance += math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)
        return distance

    def update_pheromone(self, pheromone_matrix, ant_paths):
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if i != j:
                    pheromone_matrix[i, j] *= self.rho  # 信息素挥发
                    for path in ant_paths:
                        if (i, j) in path or (j, i) in path:
                            pheromone_matrix[i, j] += self.q / self.calculate_distance(path)

    def run_aco(self):
        pheromone_matrix = np.ones((self.num_nodes, self.num_nodes))  # 初始化信息素矩阵
        best_path = []
        best_distance = float('inf')

        for _ in range(self.max_iter):
            ant_paths = []
            for ant in range(self.num_ants):
                path = []
                current_node = (0, 0)  # 从左上角开始
                path.append(current_node)
                while current_node != (self.num_nodes - 1, self.num_nodes - 1):  # 直到到达右下角
                    next_node = self.select_next_node(current_node, path, pheromone_matrix)
                    if next_node is None:
                        break
                    path.append(next_node)
                    current_node = next_node
                ant_paths.append(path)
            
            self.update_pheromone(pheromone_matrix, ant_paths)

            # 寻找最短路径
            for path in ant_paths:
                path_distance = self.calculate_distance(path)
                if path_distance < best_distance:
                    best_distance = path_distance
                    best_path = path

        return best_path, best_distance

    def select_next_node(self, current_node, path, pheromone_matrix):
        neighbors = self.get_neighbors(current_node)
        valid_neighbors = [neighbor for neighbor in neighbors if neighbor not in path and self.obstacle_matrix[neighbor] == 0]
        if not valid_neighbors:
            return None
        probabilities = []
        for neighbor in valid_neighbors:
            pheromone = pheromone_matrix[current_node[0], current_node[1]] ** self.alpha
            heuristic = (1.0 / self.calculate_distance([current_node, neighbor])) ** self.beta
            probabilities.append(pheromone * heuristic)

        probabilities = np.array(probabilities)
        probabilities /= np.sum(probabilities)
        chosen_index = np.random.choice(len(valid_neighbors), p=probabilities)
        return valid_neighbors[chosen_index]

    def get_neighbors(self, node):
        neighbors = []
        x, y = node
        # 定义上下左右四个方向
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.num_nodes and 0 <= new_y < self.num_nodes:
                neighbors.append((new_x, new_y))
        return neighbors

# 使用AntColonyOptimization类来找到最短路径
aco_solver = AntColonyOptimization(obstacle_matrix)
best_path, best_distance = aco_solver.run_aco()

print("Best Path Found:", best_path)
print("Best Distance:", best_distance)
