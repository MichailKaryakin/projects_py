import numpy as np

# Параметры системы
lambda_ = 30  # интенсивность потока заявок (1/с)
mu = 6  # производительность канала (1/с)
n = 3  # количество каналов
m = 2  # размер очереди
accuracy = 0.01  # требуемая точность


# Функция для генерации времени до следующего события
def generate_interval(intensity):
    return -np.log(1 - np.random.uniform(0, 1)) / intensity


# Имитация работы системы и итерационного процесса для достижения необходимой точности
def simulate_system(total_time, desired_accuracy, lambda_, mu, n, m):
    t = N = M = k = r = refusals = 0
    estimated_q = 0
    total_iterations = 0
    desired_accuracy_achieved = False

    while not desired_accuracy_achieved:
        while t < total_time:
            if k == 0:  # Если каналы свободны
                delta_t = generate_interval(lambda_)
                N += 1
                M += 1
                k += 1
                t += delta_t
            else:  # Если есть занятые каналы
                delta_t = generate_interval(lambda_)
                delta_tau = generate_interval(k * mu)
                if delta_t < delta_tau:  # Поступление новой заявки
                    t += delta_t
                    N += 1
                    if k < n:
                        M += 1
                        k += 1
                    elif r < m:
                        M += 1
                        r += 1
                    else:
                        refusals += 1
                else:  # Заявка обслужена
                    t += delta_tau
                    if r == 0:
                        k -= 1
                    else:
                        r -= 1
                        k = min(n, k + 1)  # Переход заявки из очереди на обслуживание

        # Расчет вероятности отказа в конце каждой итерации
        new_q = refusals / N if N > 0 else 0
        # Проверка достижения желаемой точности
        if abs(new_q - estimated_q) < desired_accuracy:
            desired_accuracy_achieved = True
            total_iterations += 1
        else:
            estimated_q = new_q
            # Увеличиваем время наблюдения для следующей итерации
            total_time += 100
            total_iterations += 1
            # Сброс счетчиков перед следующей итерацией
            t = N = M = k = r = refusals = 0

    # Итоговые значения
    return estimated_q, total_iterations, total_time


# Запуск имитации
initial_time = 100  # начальное время наблюдения для каждой итерации
estimated_q, total_iterations, simulation_time = simulate_system(initial_time, accuracy, lambda_, mu, n, m)

# Вывод результатов
print(f"Требуемое время наблюдения для достижения точности {accuracy}: {simulation_time} секунд.")
print(f"Количество итераций, которое понадобилось: {total_iterations}.")
print(f"Оценка вероятности отказа: {estimated_q:.4f}.")
