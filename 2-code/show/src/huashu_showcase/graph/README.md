# graph 模块说明

该模块用于求解哈密尔顿圆环（类 TSP）。

## 支持算法

- 动态规划（Held-Karp）：适合小规模精确求解。
- 分支限界（Branch and Bound）：可用于更大规模的启发式精确搜索。

## 接口

- `solve_hamiltonian(weight_matrix, method="dp")`

返回 `HamiltonianResult`，包含最优代价、路径和算法名称。
