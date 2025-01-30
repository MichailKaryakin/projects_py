import random
import math


def generate_exp_time(rate):
    """Генерация времени по экспоненциальному распределению"""
    return -math.log(1 - random.random()) / rate


def smo_simulation(lam, mu, observation_time):
    t = 0
    N = 0  # Всего заявок
    M = 0  # Обслуженных заявок
    while t < observation_time:
        delta_t = generate_exp_time(lam)
        delta_tau = generate_exp_time(mu)
        t += delta_t
        N += 1
        if delta_t >= delta_tau:
            M += 1
    return N, M, t  # Возвращаем также текущее время моделирования


def calculate_error(q, N, alpha=3):
    """Вычисление погрешности оценки"""
    return alpha * math.sqrt(q * (1 - q) / N)


def iterative_simulation(lam, mu, initial_time, epsilon):
    iteration = 1
    total_N, total_M, total_time = smo_simulation(lam, mu, initial_time)  # Получаем текущее время моделирования
    while True:
        q = (total_N - total_M) / total_N
        error = calculate_error(q, total_N)
        N_req, additional_time = required_observation_time(lam, mu,
                                                           error)  # Получаем требуемое количество экспериментов и
        # дополнительное время
        print(
            f"Итерация: {iteration}, Получено заявок: {total_N}, Обслужено заявок: {total_M},")
        print(
            f"Оценка вероятности отказа: {q}, Оценка погрешности: {error},")
        print(
            f"Требуемое количество опытов: {N_req}, Текущее время моделирования: {total_time}\n")

        if error <= epsilon:
            break

        additional_N, additional_M, additional_observation_time = smo_simulation(lam, mu, additional_time)
        total_N += additional_N
        total_M += additional_M
        total_time += additional_observation_time  # Обновляем общее время моделирования
        iteration += 1

    return q, total_N, total_time  # Возвращаем также общее время моделирования


def required_observation_time(lam, mu, error):
    """Вычисление необходимого времени наблюдения для заданной погрешности"""
    q_analytical = 1 - mu / lam
    N_req = (3 ** 2 * q_analytical * (1 - q_analytical)) / error ** 2
    observation_time = N_req / lam
    return N_req, observation_time  # Возвращаем количество требуемых экспериментов и время


# Параметры
lam = 30
mu = 6
initial_time = 100
epsilon = 0.01

# Итерационное моделирование
q, total_N, total_time = iterative_simulation(lam, mu, initial_time, epsilon)
print(
    f"Финальные результаты: Оценка вероятности отказа: {q},")
print(
    f"Общее количество экспериментов: {total_N}, Общее время моделирования: {total_time}")
