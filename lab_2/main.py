# Определение начальных параметров и таблицы переходов и выходов автомата Мили
TRANS = {
    ('x1', 'z1'): 'z2',
    ('x1', 'z2'): 'z3',
    ('x1', 'z3'): 'z4',
    ('x1', 'z4'): 'z1',
    ('x2', 'z1'): 'z3',
    ('x2', 'z2'): 'z4',
    ('x2', 'z3'): 'z1',
    ('x2', 'z4'): 'z2',
}

OUT = {
    ('x1', 'z1'): 'y1',
    ('x1', 'z2'): 'y2',
    ('x1', 'z3'): 'y3',
    ('x1', 'z4'): 'y4',
    ('x2', 'z1'): 'y2',
    ('x2', 'z2'): 'y3',
    ('x2', 'z3'): 'y4',
    ('x2', 'z4'): 'y1',
}

current_state = 'z1'


def mealy_machine_step(input_signal, current_state):
    next_state = TRANS[(input_signal, current_state)]
    output_signal = OUT[(input_signal, current_state)]
    return next_state, output_signal


def print_table(tact_num, inputs_history, states_history, outputs_history):
    print("\nТаблица работы автомата после такта №", tact_num)
    print("Такт:             ", list(range(1, tact_num + 1)))
    print("Входные сигналы:  ", inputs_history)
    print("Состояния:        ", states_history[:-1])  # Текущее состояние еще не изменилось
    print("Выходные сигналы: ", outputs_history)


def run_mealy_machine():
    global current_state
    inputs_history = []
    states_history = [current_state]
    outputs_history = []

    tact_num = 0  # Начинаем с такта номер 0

    while True:
        input_signal = input("Введите входной сигнал (x1 или x2): ")
        if input_signal not in ['x1', 'x2']:
            print("Неверный входной сигнал. Попробуйте снова.")
            continue

        tact_num += 1
        inputs_history.append(input_signal)
        current_state, output_signal = mealy_machine_step(input_signal, current_state)
        states_history.append(current_state)
        outputs_history.append(output_signal)

        # Выводим таблицу после каждого такта
        print_table(tact_num, inputs_history, states_history, outputs_history)

        continue_running = input("Продолжить? (да/нет): ")
        if continue_running.lower() != 'да':
            break


# Запускаем автомат Мили
run_mealy_machine()
