# 华数杯算法展示工程

<p align="center">
  <strong>遗传优化 + 层次分析 + 蚁群路径规划 + 哈密尔顿圆环</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-2f7ed8" />
  <img src="https://img.shields.io/badge/status-showcase_ready-15a34a" />
  <img src="https://img.shields.io/badge/visual-premium_dual_panel-f97316" />
  <img src="https://img.shields.io/badge/docs-fully_structured-0ea5e9" />
</p>

## 论文直达（优先入口）

- 主论文: [1-paper/机器臂关节角路径的多目标优化设计.pdf](1-paper/%E6%9C%BA%E5%99%A8%E8%87%82%E5%85%B3%E8%8A%82%E8%A7%92%E8%B7%AF%E5%BE%84%E7%9A%84%E5%A4%9A%E7%9B%AE%E6%A0%87%E4%BC%98%E5%8C%96%E8%AE%BE%E8%AE%A1.pdf)
- 题面 PDF: [1-paper/A题/2024年A题  机械臂关节角路径的优化设计.pdf](1-paper/A%E9%A2%98/2024%E5%B9%B4A%E9%A2%98%20%20%E6%9C%BA%E6%A2%B0%E8%87%82%E5%85%B3%E8%8A%82%E8%A7%92%E8%B7%AF%E5%BE%84%E7%9A%84%E4%BC%98%E5%8C%96%E8%AE%BE%E8%AE%A1.pdf)
- 题面附件: [1-paper/A题/附件.xlsx](1-paper/A%E9%A2%98/%E9%99%84%E4%BB%B6.xlsx)
- 论文与附件索引: [1-paper/README.md](1-paper/README.md)

## 核心动态展示

<table>
  <tr>
    <td width="50%" align="center">
      <img src="2-code/show/assets/gifs/robotics_grasp_2d3d.gif" alt="robotics-grasp-2d3d" width="100%" />
      <div><strong>机械臂抓取关节控制（2D/3D 联动）</strong></div>
    </td>
  </tr>
</table>

<p align="center">
  <img src="2-code/show/assets/gifs/github_cover.gif" alt="github-cover" width="960" />
</p>

## 结果与模块一键跳转

### 结果直达

- 指标汇总: [docs/results/showcase_metrics.md](docs/results/showcase_metrics.md)
- 机械臂 2D/3D 动图: [2-code/show/assets/gifs/robotics_grasp_2d3d.gif](2-code/show/assets/gifs/robotics_grasp_2d3d.gif)
- 路径优化动图: [2-code/show/assets/gifs/aco_path.gif](2-code/show/assets/gifs/aco_path.gif)
- 封面动图: [2-code/show/assets/gifs/github_cover.gif](2-code/show/assets/gifs/github_cover.gif)
- Q1 收敛图: [2-code/show/assets/figures/q1_ga_history.png](2-code/show/assets/figures/q1_ga_history.png)
- Q2 收敛图: [2-code/show/assets/figures/q2_ga_history.png](2-code/show/assets/figures/q2_ga_history.png)

### 模块代码直达

- 机械臂优化: [src/huashu_showcase/robotics](src/huashu_showcase/robotics)
- 蚁群路径规划: [src/huashu_showcase/path_planning](src/huashu_showcase/path_planning)
- 层次分析 AHP: [src/huashu_showcase/ahp](src/huashu_showcase/ahp)
- 哈密尔顿圆环: [src/huashu_showcase/graph](src/huashu_showcase/graph)
- 可视化引擎: [src/huashu_showcase/visualization](src/huashu_showcase/visualization)
- 构建脚本: [scripts](scripts)

## 最简代码分层

```text
.
├─1-paper/                                  # 论文、题面、附件
├─src/huashu_showcase/                      # 主线算法代码
│  ├─robotics/                              # 机械臂优化
│  ├─path_planning/                         # 蚁群路径规划
│  ├─ahp/                                   # 层次分析
│  ├─graph/                                 # 哈密尔顿圆环
│  └─visualization/                         # 图像与动图渲染
├─scripts/                                  # 一键构建入口
├─assets/                                   # 展示资源输出
├─docs/                                     # 说明文档
└─2-code/                                   # 历史脚本归档
   ├─robotics_legacy/
   ├─path_planning_legacy/
   ├─decision_graph_legacy/
   └─archive_docs/
```

每个子目录都已配置 README 说明，便于评审快速理解结构和职责。

## 快速构建

```bash
pip install -r requirements.txt
python scripts/build_showcase.py
```

自动更新以下产物:

- assets/gifs/github_cover.gif
- assets/gifs/robotics_grasp_2d3d.gif
- assets/gifs/ga_evolution.gif
- assets/gifs/aco_path.gif
- assets/figures/*.png
- docs/results/showcase_metrics.md

仅刷新首页核心动图:

```bash
python scripts/build_cover.py
```
