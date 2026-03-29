# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 03:19:11 2024

@author: ASUS
"""
'''
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]

    # 检查节点v是否可以加入路径path中
    def is_safe(self, v, path, pos):
        # 检查节点是否相邻且未被访问过
        if self.graph[path[pos-1]][v] == 0:
            return False

        # 检查节点是否已经在路径中
        for vertex in path:
            if vertex == v:
                return False

        return True

    # 使用回溯法寻找哈密尔顿圈
    def hamiltonian_cycle_util(self, path, pos):
        if pos == self.V:
            # 检查最后一个节点是否与起始节点相连，形成圈
            if self.graph[path[pos-1]][path[0]] == 1:
                return True
            else:
                return False

        for v in range(1, self.V):
            if self.is_safe(v, path, pos):
                path[pos] = v
                if self.hamiltonian_cycle_util(path, pos + 1):
                    return True
                path[pos] = -1

        return False

    def hamiltonian_cycle(self):
        path = [-1] * self.V

        # 从第一个节点开始，构建路径
        path[0] = 0
        if not self.hamiltonian_cycle_util(path, 1):
            print("No Hamiltonian Cycle exists")
            return False

        self.print_solution(path)
        return True

    def print_solution(self, path):
        print("Hamiltonian Cycle found:")
        for vertex in path:
            print(vertex, end=" ")
        print(path[0], "\n")


# 示例用法
g1 = Graph(5)
g1.graph = [[0, 1, 0, 1, 0],
            [1, 0, 1, 1, 1],
            [0, 1, 0, 0, 1],
            [1, 1, 0, 0, 1],
            [0, 1, 1, 1, 0]]

g1.hamiltonian_cycle()

g2 = Graph(5)
g2.graph = [[0, 1, 0, 1, 0],
            [1, 0, 1, 1, 1],
            [0, 1, 0, 0, 1],
            [1, 1, 0, 0, 0],
            [0, 1, 1, 0, 0]]

g2.hamiltonian_cycle()
'''
'''

import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Point

# 创建一个示例的geodataframe
data = {'id': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6'],
        'geometry': [Point(3, 2), Point(5, 3), Point(0, 1), Point(5, 7), Point(1, 3), Point(2, 1)]}

gdf = gpd.GeoDataFrame(data, crs='EPSG:4326')

# 构建无向图
G = nx.Graph()

# 添加点到图中
for index, row in gdf.iterrows():
    G.add_node(index, pos=(row['geometry'].x, row['geometry'].y))

# 添加边到图中（在这个示例中，任意两点之间都有一条边）
for i in range(len(gdf)):
    for j in range(i + 1, len(gdf)):
        distance = round(gdf.geometry.iat[i].distance(gdf.geometry.iat[j]),2)
        G.add_edge(i, j, weight=distance)

# 绘制图
pos = nx.get_node_attributes(G, 'pos')
labels = {index: str(gdf['id'].iloc[index]) for index in range(len(gdf))}

nx.draw(G,
        pos, 
        labels=labels,
        with_labels=True, 
        font_weight='bold', 
        node_size=200, 
        node_color='lightblue', 
        font_size=10, 
        font_color='black', 
        edge_color='gray', 
        linewidths=1, 
        alpha=0.7)

# 添加边的权重标签
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()
'''

'''优先队列法处理哈密尔顿圆（适用于点较少的？）没有遍历出来所有点，只是提取优先的处理'''
import heapq

class HamiltonianCycleSolver:
    def __init__(self, graph):
        self.graph = graph
        self.num_vertices = len(graph)
        self.min_cost = float('inf')
        self.min_path = []

    def solve(self):
        # 使用优先队列（最小堆）来实现 Branch and Bound 算法
        priority_queue = []
        initial_path = [0]  # 从顶点0开始
        initial_cost = 0
        heapq.heappush(priority_queue, (initial_cost, initial_path))

        while priority_queue:
            current_cost, current_path = heapq.heappop(priority_queue)

            # 如果当前路径已经包含了所有顶点，并且形成了一个哈密尔顿圆路径
            if len(current_path) == self.num_vertices and self.graph[current_path[-1]][current_path[0]] != 0:
                current_cost += self.graph[current_path[-1]][current_path[0]]  # 加上回到起点的权重
                if current_cost < self.min_cost:
                    self.min_cost = current_cost
                    self.min_path = current_path[:]
                continue

            # 检查每个顶点是否可以加入到当前路径中
            for vertex in range(self.num_vertices):
                if (len(current_path) < self.num_vertices and
                    vertex not in current_path and
                    self.graph[current_path[-1]][vertex] != 0):
                    
                    # 计算新路径的代价
                    new_cost = current_cost + self.graph[current_path[-1]][vertex]
                    
                    # 只将代价小于当前最小代价的路径加入优先队列
                    if new_cost < self.min_cost:
                        new_path = current_path + [vertex]
                        heapq.heappush(priority_queue, (new_cost, new_path))

        return self.min_cost, self.min_path


if __name__ == "__main__":
    # 示例带权图的邻接矩阵
    graph = [
        [0, 16, 17, 25,22,1000],
        [16, 0, 11, 1000,1000,24],
        [17, 11, 0, 10,1000,21],
        [25, 1000, 10, 0,13,15],
        [22,1000,1000,13,0,1000],
        [1000,24,21,15,1000,0]
    ]

    solver = HamiltonianCycleSolver(graph)
    min_cost, min_path = solver.solve()
    print('优先队列法：')
    print(f"最小哈密尔顿圆路径的代价为: {min_cost}")
    print(f"最小哈密尔顿圆路径为: {min_path}")
    
    
    
'''暴力搜索法,我管你那么多，全取出来比一比干一干'''
import itertools

class HamiltonianCycleSolver:
    def __init__(self, graph):
        self.graph = graph
        self.num_vertices = len(graph)
        self.min_cost = float('inf')
        self.min_path = []

    def solve(self):
        # 生成所有可能的路径
        vertices = list(range(self.num_vertices))
        for perm in itertools.permutations(vertices):
            # 计算路径的代价
            current_cost = 0
            valid_cycle = True

            for i in range(self.num_vertices):
                # 确保每条边都有权重
                if self.graph[perm[i]][perm[(i + 1) % self.num_vertices]] == 0:
                    valid_cycle = False
                    break
                current_cost += self.graph[perm[i]][perm[(i + 1) % self.num_vertices]]

            # 更新最小代价和路径
            if valid_cycle and current_cost < self.min_cost:
                self.min_cost = current_cost
                self.min_path = list(perm) + [perm[0]]

        return self.min_cost, self.min_path


if __name__ == "__main__":
    # 示例带权图的邻接矩阵
    graph = [
        [0, 16, 17, 25, 22, 1000],
        [16, 0, 11, 1000, 1000, 24],
        [17, 11, 0, 10, 1000, 21],
        [25, 1000, 10, 0, 13, 15],
        [22, 1000, 1000, 13, 0, 1000],
        [1000, 24, 21, 15, 1000, 0]
    ]

    solver = HamiltonianCycleSolver(graph)
    min_cost, min_path = solver.solve()
    print('完整搜索法：')
    print(f"最小哈密尔顿圆路径的代价为: {min_cost}")
    print(f"最小哈密尔顿圆路径为: {min_path}")




'''动态规划,我们使用一个动态规划表 dp 来存储从起点到每个子集的最小路径代价。这个表的状态可以用二元组 (mask, i) 表示，其中 mask 是当前访问的顶点集合，i 是当前顶点。

动态规划法实现'''
import numpy as np

class HamiltonianCycleSolver:
    def __init__(self, graph):
        self.graph = graph
        self.num_vertices = len(graph)
        self.inf = float('inf')

    def solve(self):
        # 动态规划表格
        dp = np.full((1 << self.num_vertices, self.num_vertices), self.inf)
        # 路径表格，用于记录路径
        path = np.full((1 << self.num_vertices, self.num_vertices), -1)
        
        # 从起点（0）开始
        dp[1][0] = 0
        
        # 遍历所有可能的子集
        for mask in range(1 << self.num_vertices):
            for u in range(self.num_vertices):
                # 只考虑 u 在当前子集中的情况
                if not (mask & (1 << u)):
                    continue
                
                # 从子集中的每个顶点 v 转移到 u
                for v in range(self.num_vertices):
                    if mask & (1 << v) and u != v and self.graph[v][u] != 0:
                        new_mask = mask ^ (1 << u)
                        if dp[new_mask][v] + self.graph[v][u] < dp[mask][u]:
                            dp[mask][u] = dp[new_mask][v] + self.graph[v][u]
                            path[mask][u] = v
        
        # 计算回到起点的最小代价
        min_cost = self.inf
        end_mask = (1 << self.num_vertices) - 1
        last_vertex = -1
        for u in range(1, self.num_vertices):
            if dp[end_mask][u] + self.graph[u][0] < min_cost:
                min_cost = dp[end_mask][u] + self.graph[u][0]
                last_vertex = u
        
        # 回溯路径
        if min_cost < self.inf:
            min_path = []
            mask = end_mask
            u = last_vertex
            while u != -1:
                min_path.append(u)
                next_vertex = path[mask][u]
                mask ^= (1 << u)
                u = next_vertex
            min_path.append(0)
            min_path.reverse()
        else:
            min_path = []
        
        return min_cost, min_path

# 示例用法
if __name__ == "__main__":
    # 示例带权图的邻接矩阵
    graph = [
        [0, 16, 17, 25, 22, 1000],
        [16, 0, 11, 1000, 1000, 24],
        [17, 11, 0, 10, 1000, 21],
        [25, 1000, 10, 0, 13, 15],
        [22, 1000, 1000, 13, 0, 1000],
        [1000, 24, 21, 15, 1000, 0]
    ]

    solver = HamiltonianCycleSolver(graph)
    min_cost, min_path = solver.solve()
    print('动态规划法：')
    print(f"最小哈密尔顿圆路径的代价为: {min_cost}")
    print(f"最小哈密尔顿圆路径为: {min_path}")

'''破圈法，分支限界法'''
import numpy as np

class BranchAndBoundSolver:
    def __init__(self, graph):
        self.graph = graph
        self.num_vertices = len(graph)
        self.inf = float('inf')
        self.best_cost = self.inf
        self.best_path = []

    def solve(self):
        # 初始化
        self.visited = [False] * self.num_vertices
        self.path = []
        self.visited[0] = True
        self.path.append(0)
        self._branch_and_bound(0, 0, 1)
        return self.best_cost, self.best_path

    def _branch_and_bound(self, current_vertex, current_cost, depth):
        # 如果所有顶点都访问过，并且回到起点，检查当前路径代价
        if depth == self.num_vertices:
            if self.graph[current_vertex][0] > 0:
                total_cost = current_cost + self.graph[current_vertex][0]
                if total_cost < self.best_cost:
                    self.best_cost = total_cost
                    self.best_path = self.path + [0]
            return
        
        # 遍历所有顶点
        for next_vertex in range(self.num_vertices):
            if not self.visited[next_vertex] and self.graph[current_vertex][next_vertex] > 0:
                # 计算当前路径代价并进入下一个状态
                new_cost = current_cost + self.graph[current_vertex][next_vertex]
                if new_cost < self.best_cost:
                    self.visited[next_vertex] = True
                    self.path.append(next_vertex)
                    self._branch_and_bound(next_vertex, new_cost, depth + 1)
                    self.path.pop()
                    self.visited[next_vertex] = False

# 示例用法
if __name__ == "__main__":
    # 示例带权图的邻接矩阵
    graph = [
        [0, 16, 17, 25, 22, 1000],
        [16, 0, 11, 1000, 1000, 24],
        [17, 11, 0, 10, 1000, 21],
        [25, 1000, 10, 0, 13, 15],
        [22, 1000, 1000, 13, 0, 1000],
        [1000, 24, 21, 15, 1000, 0]
    ]

    solver = BranchAndBoundSolver(graph)
    min_cost, min_path = solver.solve()
    print('破圈法：')
    print(f"最小哈密尔顿圆路径的代价为: {min_cost}")
    print(f"最小哈密尔顿圆路径为: {min_path}")

