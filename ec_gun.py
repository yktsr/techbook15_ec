from ec_lib import scalar_multiply
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# 有限体の素数
p = 13

# 楕円曲線の方程式
def elliptic_curve(x, a, b, p):
    return (x**3 + a * x + b) % p


# 有効な(x, y)の組み合わせを見つける関数
def find_valid_points(a, b, p):
    valid_points = []

    for x in range(p):
        y_squared = elliptic_curve(x, a, b, p)
        y = int(math.sqrt(y_squared))  # 平方根を求める
        if (y**2) % p == y_squared:
            valid_points.append((x, y))
            if y != 0:
                valid_points.append((x, p - y))  # 楕円曲線は対称なので反対側の点も追加

    point_orders = []  # 各点の位数を格納するリスト

    for x, y in valid_points:
        order = 0  # 位数を初期化
        G = (x, y)
        P = (x, y)
        while P != (None, None):  # O点に到達するまで繰り返す
            order += 1
            print("a, b", (a, b), "x, y", P, "order", order)
            P = scalar_multiply(G, order, a, p)  # Qをスカラー倍
        point_orders.append(order)

    return valid_points, point_orders


# aとbの値の範囲を指定
a_values = range(-2, 2)
b_values = range(-1, 3)

# プロット領域の初期化
fig, axes = plt.subplots(len(a_values), len(b_values), figsize=(12, 12), sharex=True, sharey=True)

for i, a in enumerate(a_values):
    for j, b in enumerate(b_values):
        valid_points, point_orders = find_valid_points(a, b, p)
        
        x_values = [point[0] for point in valid_points]
        y_values = [point[1] for point in valid_points]
        
        ax = axes[i, j]
        ax.plot(x_values, y_values, 'o', markersize=5)
        for x, y, order in zip(x_values, y_values, point_orders):
            if y == p - 1:
                ax.text(x, y - 1.3, str(order), fontsize=13, ha='center', va='bottom')
            else:
                ax.text(x, y + 0.1, str(order), fontsize=13, ha='center', va='bottom')
        ax.set_title(f'$a={a}, b={b}$')
        ax.grid(True)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.tick_params(axis='both', labelsize='large')

# レイアウト調整
plt.tight_layout()
plt.savefig('ec_curve_gun_plot.pdf', format='pdf')
plt.show()
