"""
Author: kok-s0s

信息来源
https://kok-s0s.top/index.php/archives/198/

我顺带回顾自己学过的知识，这时间我是赚的。
现在做这个思路很清晰，绝对能看懂，就是个规则罢了。
作为一个学习者最好做个学习 Note 记录下自己真正的学习 RSA 的感受。别浪费时间了花在无谓的学习。🤥

学习记录可以包含的内容
1. 其中的函数所隐含的数学思想
2. python 代码的理解（库函数使用、函数思想、循环、元组、and so on）
3. RSA 运作过程
"""

import random

max_PrimLength = 1000000000000  # 10^12 是素数的最大长度

# 欧几里德算法（gcd）又称辗转相除法，可用于计算两个整数 a, b 的最大公约数
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


# 扩展欧几里德算法：对于不全为 0 的非负整数 a，b，gcd（a，b）表示 a，b 的最大公约数，必然存在整数对 x，y ，使得 gcd(a, b) = ax + by
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


# 判断一个数是否为素数
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num ** 0.5) + 2, 2):
        if num % n == 0:
            return False
    return True


# 利用 random 模块生成随机素数（也称为质数）
def generateRandomPrim():
    while 1:
        ranPrime = random.randint(0, max_PrimLength)
        if is_prime(ranPrime):
            return ranPrime


# 生成随机的公钥和私钥
def generate_keyPairs():
    # 选取两个很大的质数
    p = generateRandomPrim()
    q = generateRandomPrim()

    # 计算 n = p * q
    n = p * q
    print("n = ", n)

    # 欧拉函数 phi(n) = (p - 1) * (q - 1)
    phi = (p - 1) * (q - 1)
    print("phi = ", phi)

    # 选择一个公开指数 e，使得 1 < e < phi(n) 且 e 与 phi(n) 互质，即 gcd(e, phi(n)) = 1，e 和 n 组合起来即为公钥，n 的长度就相当于密钥对的长度
    e = random.randint(1, phi)

    # 确保 e 与 phi(n) 互质
    g = gcd(e, phi)
    while g != 1:
        e = random.randint(1, phi)
        g = gcd(e, phi)
    print("e = ", e, " ", "phi = ", phi)

    # 计算私钥 d， e 和 d 存在互逆的关系，d 和 n 组合起来即为私钥，n 的长度就相当于密钥对的长度
    d = egcd(e, phi)[1]
    print("d = ", d)

    # 使 d 为正数
    d = d % phi
    if d < 0:
        d += phi

    return ((e, n), (d, n))


# RSA 解密
def decrypt(ctext, private_key):
    try:
        key, n = private_key
        text = [chr(pow(char, key, n)) for char in ctext]
        return "".join(text)
    except TypeError as e:
        print(e)


# RSA 加密
def encrypt(text, public_key):
    key, n = public_key
    ctext = [pow(ord(char), key, n) for char in text]
    return ctext


# RSA 加密和解密互逆
if __name__ == "__main__":
    public_key, private_key = generate_keyPairs()
    print("Public: ", public_key)
    print("Private: ", private_key)

    ctext = encrypt("kok-s0s", public_key)
    print("encrypted =", ctext)
    plaintext = decrypt(ctext, private_key)
    print("decrypted =", plaintext)
