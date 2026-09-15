import matplotlib.pyplot as plt
import numpy as np

### 1.定义一个透镜
R1 = 50 # 前表面曲率半径
R2 = -50 # 后表面曲率半径)
thickness = 5 # 透镜中心厚度
diameter = 40 # 透镜直径
n = 1.5 # 透镜折射率
semi_diameter = diameter / 2

### 2.定义弓高sag函数
def sag(y,R):
    R_abs = abs(R)
    return R_abs - np.sqrt(R**2 - y**2)

### 3.计算前后
# =========================
# 绘图
# =========================
plt.figure(figsize=(10, 6))

## 1.画出透镜
