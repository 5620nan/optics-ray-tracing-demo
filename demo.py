import numpy as np
import matplotlib.pyplot as plt
# =========================
# 1. 设置透镜参数
# =========================
f = 50.0          # 焦距，单位：mm
lens_x = 0.0      # 透镜所在位置
lens_radius = 20  # 透镜半径

# =========================
# 2. 生成平行光线
# =========================
# 在透镜上下生成若干条平行光线
ray_heights = np.linspace(-15, 15, 11)

rays = []

for y in ray_heights:
    # 光线起点
    x_start = -100
    # 平行光沿 x 方向传播
    rays.append({
        "x": x_start,
        "y": y
    })

# =========================
# 3. 计算光线经过凸透镜后的方向
# =========================
refracted_rays = []

for ray in rays:

    y = ray["y"]

    # 薄透镜近似：
    # 平行光经过透镜后指向焦点 (f, 0)

    x1 = lens_x
    y1 = y

    x2 = lens_x + f
    y2 = 0

    # 光线方向
    dx = x2 - x1
    dy = y2 - y1

    # 单位方向向量
    length = np.sqrt(dx**2 + dy**2)

    dx = dx / length
    dy = dy / length

    refracted_rays.append({
        "x": x1,
        "y": y1,
        "dx": dx,
        "dy": dy
    })

# =========================
# 4. 绘图
# =========================
plt.figure(figsize=(10, 6))

# ---- 绘制入射光线 ----

for ray in rays:
    x1 = ray["x"]
    y1 = ray["y"]

    x2 = lens_x
    y2 = y1

    plt.plot(
        [x1, x2],
        [y1, y2],
        linewidth=1
    )


# ---- 绘制折射后的光线 ----

for ray in refracted_rays:

    x1 = ray["x"]
    y1 = ray["y"]

    # 为了画图，让光线继续传播 70 mm
    x2 = x1 + 70 * ray["dx"]
    y2 = y1 + 70 * ray["dy"]

    plt.plot(
        [x1, x2],
        [y1, y2],
        linewidth=1
    )


# ---- 绘制透镜 ----

lens_y = np.linspace(-lens_radius, lens_radius, 100)

# 简单画成竖直线
plt.plot(
    np.zeros_like(lens_y),
    lens_y,
    linewidth=4
)


# ---- 绘制焦点 ----

plt.scatter(
    [lens_x + f],
    [0],
    s=80,
    zorder=5
)

plt.text(
    lens_x + f + 2,
    1,
    "Focus"
)


# ---- 光轴 ----

plt.axhline(
    y=0,
    linestyle="--",
    linewidth=0.8
)


# ---- 坐标设置 ----

plt.xlabel("x (mm)")
plt.ylabel("y (mm)")
plt.title("Parallel Rays Through a Convex Lens")

plt.axis("equal")
plt.grid(True)

plt.show()