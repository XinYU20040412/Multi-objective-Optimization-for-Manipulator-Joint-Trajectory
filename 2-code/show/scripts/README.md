# scripts 目录说明

该目录负责从算法模块生成最终可展示产物。

## 脚本列表

- `build_showcase.py`: 一键生成全部图像、GIF 和结果汇总文档。
- `build_cover.py`: 快速刷新首页核心动图（封面总览 + 机械臂 2D/3D 抓取控制）。

## 典型流程

```bash
python scripts/build_showcase.py
```

运行后可直接将 `assets/` 目录中的资源在 README 中引用。

## 封面动图说明

`assets/gifs/github_cover.gif` 由 `build_showcase.py` 和 `build_cover.py` 自动生成，
用于 GitHub 首页第一屏展示，不运行代码也能看懂优化过程与结果。

`assets/gifs/robotics_grasp_2d3d.gif` 同样由脚本自动生成，
用于展示机械臂关节控制下的抓取过程（2D 轨迹 + 3D 姿态联动）。
