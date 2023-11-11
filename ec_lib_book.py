# 2つの楕円曲線上の点を加算する関数
# 無限遠点Oは(None, None)と表現されている
def add_points(P, Q, a, p):
    # 条件 d)
    if Q == (None, None):
        # P + O = P
        return P
    if P == (None, None):
        # Q + O = Q
        return Q

    x_p, y_p = P
    x_q, y_q = Q

    # 条件 c)
    if x_p == x_q and ((y_p + y_q) % p == 0):
        return (None, None)

    if P == Q:
        # 条件 b)
        m = ((3 * x_p**2 + a) * pow(2 * y_p, -1, p)) % p
    else:
        # 条件 a)
        m = ((y_q - y_p) * pow(x_q - x_p, -1, p)) % p

    x_r = (m**2 - x_p - x_q) % p
    y_r = (m * (x_p - x_r) - y_p) % p

    return (x_r, y_r)


# スカラー倍の関数
# 例えば 7P を計算する際に、単に繰り返し加算をして 7P = P + P + ... + P + P を計算してもよいが、
# 7Pは、4P + 2P + P とも表現できる。
# この方法をバイナリ法（繰り返し2乗法）と呼び、Pが大きいほど効率的に解が得られる。
def scalar_multiply(P, n, a, p):
    Q = (None, None)
    for i in range(n.bit_length()):
        if n & (1 << i):
            Q = add_points(Q, P, a, p)
        P = add_points(P, P, a, p)
    return Q

a = -1
b = 2
p = 13

# 生成元の座標
G = (6, 11)

points = []
for j in range(p):
    nG = scalar_multiply(G, j + 1, a, p)
    points.append(nG)
    print(f"{j + 1}G =", nG)
    if nG == (None, None):
        # 無限遠点に到達したら打ち切り
        break
print('<G_{}> = {}'.format(G, points))
