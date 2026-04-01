# scripts 目录说明

该目录负责从算法模块生成最终可展示产物。

## 脚本列表

- `build_showcase.py`: 一键生成全部图像、GIF 和结果汇总文档。
- `build_cover.py`: 快速刷新 GitHub 封面 GIF（GA 收敛 + 参数轨迹 + ACO 路径扩展同屏）。

## 典型流程

```bash
python scripts/build_showcase.py
```

运行后可直接将 `assets/` 目录中的资源在 README 中引用。

## 封面动图说明

`assets/gifs/github_cover.gif` 由 `build_showcase.py` 和 `build_cover.py` 自动生成，
用于 GitHub 首页第一屏展示，不运行代码也能看懂优化过程与结果。
