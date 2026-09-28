import matplotlib.pyplot as plt
import numpy as np

# 一、画一个凸透镜

## 1.定义一个透镜
R1 = 50 # 前表面曲率半径
R2 = -50 # 后表面曲率半径)
thickness = 5 # 透镜中心厚度
diameter = 20 # 透镜直径
n1 = 1.0 # 空气折射率
n2 = 1.5 # 透镜折射率
semi_diameter = diameter / 2 # 半口径
y_lens = np.linspace(-semi_diameter, semi_diameter, 400) # 在半口径范围内取400个y点

## 2.定义弓高sag函数
def sag(y_lens,R):
    R_abs = abs(R)
    return R_abs - np.sqrt(R ** 2 - y_lens ** 2)

## 3.计算前后表面曲线
x_v1 = 0 # 前表面顶点坐标
y_v1 = 0
x_front = 0 + sag(y_lens,R1) # 前表面曲线
x_back = thickness - sag(y_lens, R2)  #计算后表面曲线

x_v2 = thickness # 后表面顶点坐标
y_v2 = 0

## 4.绘制
plt.figure(figsize=(10, 6)) # 定义一张画布
### 1.画出前后表面
plt.plot(x_front,y_lens,label = "Front Surface")
plt.plot(x_back,y_lens,label = "Back Surface")

### 2.填充内部
plt.fill_betweenx(y_lens,x_front,x_back,alpha = 0.5)

### 3.画出光轴
plt.axhline(0,linestyle = "--",linewidth = 0.8)

### 4.标出前后顶点
plt.scatter([thickness,0],[0,0],s = 40)
plt.text(0,0.8,'V1')
plt.text(thickness,0.8,'V2')

### 5.图形设置
plt.title("Biconvex Lens")
plt.xlabel("x(mm)")
plt.ylabel("y(mm)")
plt.axis('equal')
plt.grid(True)
plt.legend()


# 二、生成平行光线并对其追迹
## 1.生成平行光并与凸透镜前表面相交
ray = {
    'x' : -20,
    'dx' : 1,
    'dy' : 0,
}

num_rays = 11
ray_heights = np.linspace(
    -semi_diameter * 0.9,
    semi_diameter * 0.9,
    num_rays
)

y0 = 0 #光线起始y
for y0 in ray_heights:
    x0 = ray["x"]
    dx = ray['dx'] #光线x传播方向
    dy = ray['dy'] # 光线y传播方向

    t = np.linspace(0,20,100)

    x_ray = x0 + t * dx #光线参数方程
    y_ray = y0 + t * dy

    ## 2.求平行光与前表面交点
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
        t_root1 = (-B + np.sqrt(delta))/(2 * A) # 求出平行光与圆相交时的t
        t_root2 = (-B - np.sqrt(delta))/(2 * A)

    x_root1 = x0 + t_root1 * dx # 根据求出的t，求出光线与凸透镜前表面交点横坐标
    y_root1 = y0 + t_root1 * dy
    x_root2 = x0 + t_root2 * dx
    y_root2 = y0 +t_root2 * dy

    distance_1 = abs(x_v1 - x_root1) # 选择与前表面顶点差值更小的点作为交点
    distance_2 = abs(x_v1 - x_root2)
    if distance_1 < distance_2:
        x_hit = x_root1
        y_hit = y_root1
    else:
        x_hit = x_root2
        y_hit = y_root2

    ## 3.求入射向量和入射点法向量
    I = np.array([dx, dy]) # 入射光线方向向量

    nx = x_c1 - x_hit
    ny = y_c1 - y_hit

    length = np.sqrt(nx ** 2 + ny ** 2) # 求出向量模长

    nx = nx / length # 求出法向量的方向向量
    ny = ny / length

    N = np.array([nx,ny]) # 前表面顶点法向量方向向量

    ## 4.根据斯涅尔定律求折射方向角/方向向量
    cos_theta1 = np.dot(I,N)
    sin_theta1 = np.sqrt(1 - cos_theta1 ** 2) # 求出入射角sin值
    eta = n1 / n2

    sin_theta2 = n1 / n2 * sin_theta1 # 根据斯涅尔定律求出折射角
    cos_theta2 = np.sqrt(1 - sin_theta2 ** 2)
    theta2 = np.arcsin(sin_theta2)

    T = eta * I + (cos_theta2 - eta * cos_theta1) * N # 折射方向向量

    dx2 = T[0]
    dy2 = T[1]

    # ## 5.继续创建折射光线的光线参数方程
    ray_length = 30
    x_ref_end = x_hit + ray_length * dx2  # 折射光线的光线参数方程
    y_ref_end = y_hit + ray_length * dy2

    ## 6.求出折射光线和后表面交点
    x_c2 = x_v2 + R2
    y_c2 = 0

    A = dx2 ** 2 + dy2 ** 2
    B = 2 * (
            (x_hit - x_c2) * dx2 + (y_hit + y_c2) * dy2
    )
    C = (x_hit - x_c2) ** 2 + (y_hit - y_c2) ** 2 - R2 ** 2


    delta = B ** 2 - 4 * A * C

    if delta < 0:
        print("光线没有与圆相交")
    else:
        ray_length_root1 = (-B + np.sqrt(delta))/(2 * A) # 求出平行光与圆相交时的t
        ray_length_root2= (-B - np.sqrt(delta))/(2 * A)

    x_ref_end_root1 = x_hit + ray_length_root1 * dx2 # 根据求出的t，求出光线与凸透镜前表面交点横坐标
    y_ref_end_root1 = y_hit + ray_length_root1 * dy2
    x_ref_end_root2 = x_hit + ray_length_root2 * dx2
    y_ref_end_root2 = y_hit + ray_length_root2 * dy2

    distance_3 = abs(x_v2 - x_ref_end_root1) # 选择与后表面顶点差值更小的点作为交点
    distance_4 = abs(x_v2 - x_ref_end_root2)

    if distance_3 < distance_4:
        x_ref_end = x_ref_end_root1
        y_ref_end = y_ref_end_root1
    else:
        x_ref_end = x_ref_end_root2
        y_ref_end = y_ref_end_root2

    ## 7.再次利用斯涅尔定律，求出出射方向向量
    I_ref = N

    nx_back = x_ref_end - x_c2 # 折射终点法向量法向量
    ny_back = y_ref_end - y_c2
    length_N_ref = np.sqrt(nx_back ** 2 + ny_back ** 2)
    nx_back = nx_back / length_N_ref
    ny_back = ny_back / length_N_ref
    N_ref = np.array([nx_back, ny_back])

    N_ref = np.array([nx_back, ny_back])

    ## 8.求出出射光线参数方程

    cos_theta_ref = np.dot(I_ref,N_ref)
    sin_theta_ref = np.sqrt(1 - cos_theta_ref ** 2) # 求出折射终点角sin值
    cos_theta_ref = np.clip(cos_theta_ref, -1.0, 1.0)
    eta_ref = n2 / n1

    sin_theta_exit = n2 / n1 * sin_theta_ref # 根据斯涅尔定律求出出射角

    if sin_theta_exit > 1:
        print("发生全反射")

    cos_theta_exit = np.sqrt(1 - sin_theta_exit ** 2)

    T_exit = eta_ref * I_ref + (cos_theta_exit - eta_ref * cos_theta_ref) * N_ref # 出射方向向量

    T_exit = T_exit / np.linalg.norm(T_exit)

    dx_exit = T_exit[0]
    dy_exit = T_exit[1]

    t_out = np.linspace(0, 100, 100)

    x_exit = x_ref_end + t_out * dx_exit # 出射光线参数方程
    y_exit = y_ref_end + t_out * dy_exit

    t_out = - y_ref_end / dy_exit
    x_focus = x_ref_end + t_out * dx_exit

    ## 绘制
    plt.scatter([x_hit], [y_hit], s = 40)
    plt.scatter([x_ref_end], [y_ref_end], s = 40)


    plt.plot(x_ray,y_ray,linestyle = "--")
    plt.plot(
        [x_hit, x_ref_end],
        [y_hit, y_ref_end],
        "r--",
        label="Refracted Ray"
    )
    plt.plot(
        [x_ref_end, x_focus],
        [y_ref_end, 0],
        "r--",
        label="Refracted Ray"
    )
    plt.scatter([x_focus], [0], s = 40)
    plt.text(x_focus,0,'focus')
plt.show()