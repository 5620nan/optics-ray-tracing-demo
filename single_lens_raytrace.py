import matplotlib.pyplot as plt
import numpy as np
# 一、画一个凸透镜

# =========================
# 定义一个透镜
# =========================
## 1.定义一个透镜
R1 = 50 # 前表面曲率半径
R2 = -50 # 后表面曲率半径)
t = 5 # 透镜中心厚度
diameter = 20 # 透镜直径
n = 1.5 # 透镜折射率
semi_diameter = diameter / 2 # 半口径
y = np.linspace(-semi_diameter, semi_diameter, 400) # 在半口径范围内取400个y点

## 2.定义弓高sag函数
def sag(y,R):
    R_abs = abs(R)
    return R_abs - np.sqrt(R**2 - y**2)

## 3.计算前后表面曲线
x_front = 0 + sag(y,R1) # 前表面曲线
x_back = t - sag(y, R2)  #计算后表面曲线


# =========================
# 绘图
# =========================
plt.figure(figsize=(10, 6)) # 定义一张画布

## 1.画出前后表面
plt.plot(x_front,y,label = "Front Surface")
plt.plot(x_back,y,label = "Back Surface")

## 2.填充内部
plt.fill_betweenx(y,x_front,x_back,alpha = 0.5)

## 3.画出光轴
plt.axhline(0,linestyle = "--",linewidth = 0.8)

## 4.标出前后顶点
plt.scatter([t,0],[0,0],s = 40)
plt.text(0,0.8,'V1')
plt.text(t,0.8,'V2')

## 5.图形设置
plt.title("Biconvex Lens")
plt.xlabel("x(mm)")
plt.ylabel("y(mm)")
plt.axis('equal')
plt.grid(True)
plt.legend()

plt.show()