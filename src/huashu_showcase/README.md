# huashu_showcase 包说明

该包提供华数杯相关算法的统一接口。

## 使用方式

```python
from huashu_showcase.robotics import run_question1, run_question2
from huashu_showcase.ahp import compute_ahp
```

## 包级原则

- 每个子模块独立可运行。
- 结果对象结构化返回，不依赖 print 侧输出。
- 输入参数尽量显式，减少魔法常量。
