# robotics 模块说明

该模块整合第一问与第二问的机械臂优化建模。

## 文件说明

- `model.py`: 机械臂运动学、末端误差、重力势能与能耗计算。
- `ga.py`: 通用遗传算法优化器（最小化问题）。
- `pipeline.py`: 问题级入口（`run_question1` / `run_question2`）。

## 优化点

- 去除原脚本重复的矩阵计算函数。
- 使用 `atan2` 提升姿态角求解的数值稳定性。
- 将能耗积分等价为闭式表达，减少积分开销。

## 输出结果

`run_question1` 和 `run_question2` 返回 `RoboticsOptimizationResult`，包含：

- 最优参数与轨迹
- 收敛历史
- 末端误差
- 重力做功
- 各关节与总能耗
