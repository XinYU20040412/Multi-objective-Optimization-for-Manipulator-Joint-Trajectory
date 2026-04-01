# src 目录说明

`src` 是全部可复用算法代码的源码根目录，采用标准 Python `src layout`。

## 设计目标

- 代码按算法域拆分，避免单文件混合多题逻辑。
- 所有核心功能都可被脚本调用，也可在 Notebook/其他项目中导入。
- 模块内尽量纯函数化，提升可测试性。

## 子目录

- `huashu_showcase/ahp`: 层次分析法
- `huashu_showcase/robotics`: 机械臂模型与遗传优化
- `huashu_showcase/graph`: 哈密尔顿圆环求解
- `huashu_showcase/path_planning`: 蚁群路径规划
- `huashu_showcase/visualization`: 可视化与 GIF 导出
