import math

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kstest
import time

# Инициализация генератора случайных чисел
np.random.seed(int(time.time()))

# Функция для генерации случайных чисел с заданным распределением
def generate_random_numbers(n, a=0, b=math.tan(1)):
    return a + (b - a) * np.sqrt(np.random.uniform(size=n))

# Теоретическая функция распределения
def theoretical_distribution(x, a=0, b=math.tan(1)):
    x = np.asarray(x)
    result = np.zeros_like(x)

    mask = (x >= a) & (x <= b)
    result[mask] = ((x[mask] - a) / (b - a)) ** 2

    mask = x > b
    result[mask] = 1

    return result

# Функция для сравнения статистической и теоретической функций распределения
def compare_distributions(samples, theoretical_func):
    sorted_samples = np.sort(samples)
    empirical_cdf = np.arange(1, len(samples) + 1) / len(samples)
    theoretical_cdf = np.array([theoretical_func(x) for x in sorted_samples])
    delta = np.max(np.abs(empirical_cdf - theoretical_cdf))

    plt.step(sorted_samples, empirical_cdf, where='post', label='Эмпирическая КРФ')
    plt.plot(sorted_samples, theoretical_cdf, label='Теоретическая КРФ', linestyle='--')
    plt.xlabel('Значение выборки')
    plt.ylabel('КРФ')
    plt.title('Сравнение Эмпирической и Статистической КРФ')
    plt.legend()
    plt.show()

    return delta

# Функция для оценки математического ожидания и дисперсии
def estimate_mean_and_variance(samples):
    mean = np.mean(samples)
    variance = np.var(samples)
    return mean, variance

# Пример использования
sample_sizes = [50, 100, 1000, 10**5]
for size in sample_sizes:
    samples = generate_random_numbers(size)
    mean, variance = estimate_mean_and_variance(samples)
    print(f'Размер выборки: {size}, Среднее: {mean}, Дисперсия: {variance}')

    statistic, p_value = kstest(samples, lambda x: theoretical_distribution(x))
    print(f'Тест по критерию Колмогорова: Статистика = {statistic}, P-value = {p_value}')

    delta = compare_distributions(samples, theoretical_distribution)
    print(f'Максимальное отклонение (Дельта): {delta}')
