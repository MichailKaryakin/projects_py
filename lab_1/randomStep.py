import numpy as np
import matplotlib.pyplot as plt


# Функция модели системы дифференциальных уравнений
def model(t, y, p, a, m, u, cx, cy, m1, m2, g):
    x1, x2, x3, x4, x5 = y
    dx1dt = -g * np.sin(x2) + (p - a * cx * x1 ** 2) / (m - u * t)
    dx2dt = (-g + (p * np.sin(x5 - x2) + a * cy * x1 ** 2) / (m - u * t)) / x1
    dx3dt = (m1 * a * (x2 - x5) * x1 ** 2 - m2 * a * x1 ** 2 * x3) / (m - u * t)
    dx4dt = x1 * np.sin(x2)
    dx5dt = x3
    return [dx1dt, dx2dt, dx3dt, dx4dt, dx5dt]


# Метод Эйлера для интегрирования системы уравнений с заданным шагом
def euler_method(h, model, y0, T, g, p, a, m, u, cx, cy, m1, m2):
    N = int(T / h) + 1
    t = np.linspace(0, T, N)
    y = np.zeros((N, len(y0)))
    y[0] = y0
    for i in range(1, N):
        y[i] = y[i - 1] + h * np.array(model(t[i - 1], y[i - 1], p, a, m, u, cx, cy, m1, m2, g))
    return t, y


# Начальные условия и параметры модели
y0 = [1500, 1, 0, 0, 1]
p = 50000
a = 1.1
m = 2000
u = 50
cx = 0.02
cy = 0.005
m1 = 0.05
m2 = 0.005
g = 9.81
T = 14

# Заданный шаг интегрирования
h = float(input("введите шаг"))

# Вычисление решения с заданным шагом
t, y = euler_method(h, model, y0, T, g, p, a, m, u, cx, cy, m1, m2)

# Вывод графиков для каждой переменной
fig, axs = plt.subplots(5, 1, figsize=(10, 15))

axs[0].plot(t, y[:, 0], label='x1')
axs[0].set_title('x1(t)')
axs[0].grid(True)

axs[1].plot(t, y[:, 1], label='x2', color='g')
axs[1].set_title('x2(t)')
axs[1].grid(True)

axs[2].plot(t, y[:, 2], label='x3', color='r')
axs[2].set_title('x3(t)')
axs[2].grid(True)

axs[3].plot(t, y[:, 3], label='x4', color='c')
axs[3].set_title('x4(t)')
axs[3].grid(True)

axs[4].plot(t, y[:, 4], label='x5', color='m')
axs[4].set_title('x5(t)')
axs[4].grid(True)

for ax in axs:
    ax.legend()

plt.tight_layout()
plt.show()
