import matplotlib.pyplot as plt
import numpy as np
from fontTools.ttLib.tables.V_D_M_X_ import table_V_D_M_X_

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
x_v1 = 0 # 前表面顶点坐标
y_v1 = 0
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



# 二、生成一条平行光线并对其追迹
## 生成一条平行光并与凸透镜前表面相交
ray = {
    'x' : -20,
    'y' : np.random.uniform(-9,9,1),
    'dx' : 1,
    'dy' : 0,
}

x0 = ray['x'] #光线起始x
y0 = ray['y'] #光线起始y
dx = ray['dx'] #光线x传播方向
dy = ray['dy'] # 光线y传播方向

t = np.linspace(0,20,100)

x = x0 + t * dx #光线参数方程
y = y0 + t * dy


## 求平行光与前表面交点
x_c1 = x_v1 + R1 #凸透镜前表面圆心坐标
y_c1 = 0

A = dx ** 2 + dy ** 2
B = 2 * (
        (x0 - x_c1) * dx + (y0 + y_c1) * dy
)
C = (x0 - x_c1) ** 2 + (y0 - y_c1) ** 2 - R1 ** 2


delta = B ** 2 - 4 * A * C

if delta < 0:
    print("光线没有与圆相交")
else:
    t1 = (-B + np.sqrt(delta))/(2 * A) # 求出平行光与圆相交时的t
    t2 = (-B - np.sqrt(delta))/(2 * A)

x1 = x0 + t1 * dx # 根据求出的t，求出光线与凸透镜前表面交点横坐标
x2 = x0 + t2 * dx

distance_1 = abs(x_c1 - x1) # 选择与前表面顶点差值更小的点作为交点
distance_2 = abs(x_c1 - x2)
if distance_1 < distance_2:
    x_hit = x1
else:
    x_hit = x2

y_hit = y0

plt.scatter([x_hit],[y_hit],s = 40)
plt.plot(x,y,linestyle = "--")
plt.show()