import numpy as np
import matplotlib.pyplot as plt


# Функция модели системы дифференциальных уравнений
def model(t, y):
    x1, x2, x3, x4, x5 = y
    dx1dt = -g * np.sin(x2) + (p - a * cx * x1 ** 2) / (m - u * t)
    dx2dt = (-g + (p * np.sin(x5 - x2) + a * cy * x1 ** 2) / (m - u * t)) / x1
    dx3dt = (m1 * a * (x2 - x5) * x1 ** 2 - m2 * a * x1 ** 2 * x3) / (m - u * t)
    dx4dt = x1 * np.sin(x2)
    dx5dt = x3
    return [dx1dt, dx2dt, dx3dt, dx4dt, dx5dt]


# Метод Эйлера для интегрирования системы уравнений
def euler_method(h):
    N = int(T / h) + 1
    t = np.linspace(0, T, N)
    y = np.zeros((N, len(y0)))
    y[0] = y0
    for i in range(1, N):
        y[i] = y[i - 1] + h * np.array(model(t[i - 1], y[i - 1]))
    return t, y


# Функция оценки погрешности
def estimate_error(y, y_half):
    y_end = y[-1, 3]  # x4(T) при шаге h
    y_half_end = y_half[-1, 3]  # x4(T) при шаге h/2
    abs_error = np.abs(y_half_end - y_end)
    rel_error = abs_error / np.abs(y_half_end) * 100
    return abs_error, rel_error


# Функция для анализа точности и трудоемкости
def analyze_accuracy_and_workload(h_initial, T):
    h_values = []
    rel_errors = []
    workload_estimations = []
    h = h_initial
    while h > 1e-4:
        t, y = euler_method(h)
        t_half, y_half = euler_method(h / 2)
        _, rel_error = estimate_error(y, y_half)
        h_values.append(h)
        rel_errors.append(rel_error)
        workload_estimations.append(len(t))
        h /= 2

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(h_values, rel_errors, marker='o')
    plt.xlabel('Шаг интегрирования h')
    plt.ylabel('Относительная погрешность (%)')
    plt.title('Зависимость относительной погрешности от шага')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(h_values, workload_estimations, marker='o')
    plt.xlabel('Шаг интегрирования h')
    plt.ylabel('Оценка трудоемкости (количество шагов)')
    plt.title('Зависимость трудоемкости от шага')
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# Автоматический выбор шага интегрирования
def auto_step_selection(h_initial, error_threshold):
    h = h_initial
    rel_error = 100
    while rel_error > error_threshold:
        t, y = euler_method(h)
        t_half, y_half = euler_method(h / 2)
        _, rel_error = estimate_error(y, y_half)
        h /= 2
    return h, t, y


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
h_initial = 0.1

# Выполнение интегрирования и анализа
analyze_accuracy_and_workload(h_initial, T)

# Выбор оптимального шага и вывод результатов
error_threshold = 1
h_optimal, t_optimal, y_optimal = auto_step_selection(h_initial, error_threshold)
plt.figure(figsize=(10, 8))
for i in range(5):
    plt.plot(t_optimal, y_optimal[:, i], label=f'x{i + 1}')
plt.xlabel('Время (с)')
plt.ylabel('Значения переменных')
plt.title('Решение системы дифференциальных уравнений')
plt.legend()
plt.grid(True)
plt.show()

x4_T = y_optimal[-1, 3]
print(f"x4(T) = {x4_T}")
_, rel_error_optimal = estimate_error(y_optimal, euler_method(h_optimal / 2)[1])
print(f"Относительная погрешность: {rel_error_optimal}%")
# Расширение кода для рисования отдельных графиков для каждой переменной

# Вывод графиков для каждой переменной
fig, axs = plt.subplots(5, 1, figsize=(10, 15))

axs[0].plot(t_optimal, y_optimal[:, 0], label='x1')
axs[0].set_title('x1(t)')
axs[0].grid(True)

axs[1].plot(t_optimal, y_optimal[:, 1], label='x2', color='g')
axs[1].set_title('x2(t)')
axs[1].grid(True)

axs[2].plot(t_optimal, y_optimal[:, 2], label='x3', color='r')
axs[2].set_title('x3(t)')
axs[2].grid(True)

axs[3].plot(t_optimal, y_optimal[:, 3], label='x4', color='c')
axs[3].set_title('x4(t)')
axs[3].grid(True)

axs[4].plot(t_optimal, y_optimal[:, 4], label='x5', color='m')
axs[4].set_title('x5(t)')
axs[4].grid(True)

for ax in axs:
    ax.legend()

plt.tight_layout()
plt.show()
