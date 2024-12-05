import numpy as np
import L_matrix 
from munkres import Munkres

def generate_bij(l, beta1, beta2, distribution_type, delta_values=None, ripening=True, v=None):
    B = np.zeros((l, l))
    beta_max = 1.15

    if distribution_type == "u":
        # Равномерное распределение на отрезке [beta1, beta2]
        for i in range(l):
            for j in range(l):
                if ripening and j < v:
                    B[i, j] = np.random.uniform(1, beta_max)  # Дозаривание
                else:
                    B[i, j] = np.random.uniform(beta1, beta2)  # Без дозаривания
    elif distribution_type == "c":
        # Концентрированное распределение
        for i in range(l):
            delta_i = delta_values[i]
            # Проверка, что delta_i не превышает ограничения
            if delta_i > (beta2 - beta1) / 4:
                raise ValueError(f"Для i={i} значение delta_i должно быть <= (beta2 - beta1) / 4.")
            
            beta_i1 = np.random.uniform(beta1, beta2 - delta_i)
            beta_i2 = beta_i1 + delta_i

            for j in range(l):
                B[i, j] = np.random.uniform(beta_i1, beta_i2)  # Генерация значений для концентрированного распределения
    else:
        raise ValueError("Неизвестный тип распределения. Используйте 'uniform' или 'concentrated'.")

    return B

def generate_c_matrix(a_min, a_max, B):
    """
    Функция для генерации матрицы состояний C на основе начальных значений a_i и коэффициентов деградации B.

    a_min, a_max - диапазон начальных значений a_i (доли сахара в начальном сырье)
    B - матрица коэффициентов деградации

    Возвращает матрицу C.
    """
    n = B.shape[0]  # Количество партий (строк)

    # Генерация начальных значений a_i
    a = np.random.uniform(a_min, a_max, n)

    # Инициализация матрицы C
    C = np.zeros((n, n))

    for i in range(n):
        C[i, 0] = a[i]  # Установка начального значения a_i
        for j in range(1, n):
            C[i, j] = C[i, j - 1] * B[i, j - 1]  # Последовательное умножение

    return C

def Maximum(S):
    """Венгерский максимум"""
    cost_matrix = cost_matrix.transpose()
    row_indices, col_indices = linear_sum_assignment(cost_matrix)
    col_values = [-cost_matrix[i, col_indices[i]] for i in range(len(row_indices))]
    max_sum = abs(cost_matrix[row_indices, col_indices].sum()) 
    return max_sum

def Minimum(S):
    """Венгерский минимум"""
    cost_matrix = cost_matrix.transpose()
    row_indices, col_indices = linear_sum_assignment(cost_matrix) 
    col_values = [cost_matrix[i, col_indices[i]] for i in range(len(row_indices))] 
    min_sum = cost_matrix[row_indices, col_indices].sum() 
    return min_sum

def thrifty_strategy(matrix):
    """Бережливая стратегия: на каждом этапе выбираем партию с наименьшей ценностью."""
    calc_matrix = matrix.copy()
    num_batches, num_stages = calc_matrix.shape
    selected_order = []
    
    for j in range(num_stages):
        # Choosing the batch with the minimum value at the current stage
        min_index = np.argmin(calc_matrix[:, j])
        selected_order.append(min_index)
        # Removing the selected batch from future stages
        calc_matrix[min_index, :] = np.inf
    
    final_value = calculate_final_value(matrix, selected_order)
    return final_value

def greedy_strategy(matrix):
    """Жадная стратегия: на каждом этапе выбираем партию с наибольшей ценностью."""
    calc_matrix = matrix.copy()
    num_batches, num_stages = calc_matrix.shape
    selected_order = []
    
    for j in range(num_stages):
        # Choosing the batch with the maximum value at the current stage
        max_index = np.argmax(calc_matrix[:, j])
        selected_order.append(max_index)
        # Removing the selected batch from future stages
        calc_matrix[max_index, :] = -np.inf
    
    final_value = calculate_final_value(matrix, selected_order)
    return final_value

def tg_strategy(matrix, v):
    """Стратегия Thrifty-Greedy: первые v-1 этапов - бережливая, начиная с v - жадная."""
    calc_matrix = matrix.copy()
    num_batches, num_stages = calc_matrix.shape
    selected_order = []

    for j in range(v):
        min_index = np.argmin(calc_matrix[:, j])
        selected_order.append(min_index)
        calc_matrix[min_index, :] = np.inf

    for j in range(num_batches):
        if calc_matrix[j, 0] == np.inf:
            calc_matrix[j, :] = -np.inf

    for j in range(v, num_stages):
        max_index = np.argmax(calc_matrix[:, j])
        selected_order.append(max_index)
        calc_matrix[max_index, :] = -np.inf
    
    final_value = calculate_final_value(matrix, selected_order)
    return final_value

def gt_strategy(matrix, v):
    """Стратегия Greedy-Thrifty: первые v-1 этапов - жадная, начиная с v - бережливая."""
    calc_matrix = matrix.copy()
    num_batches, num_stages = calc_matrix.shape
    selected_order = []
    
    for j in range(v):
        max_index = np.argmax(calc_matrix[:, j])
        selected_order.append(max_index)
        calc_matrix[max_index, :] = -np.inf
        
    for j in range(num_batches):
        if calc_matrix[j, 0] == -np.inf:
            calc_matrix[j, :] = np.inf
            
    for j in range(v, num_stages):
        min_index = np.argmin(calc_matrix[:, j])
        selected_order.append(min_index)
        calc_matrix[min_index, :] = np.inf
    
    final_value = calculate_final_value(matrix, selected_order)
    return final_value

def calculate_final_value(matrix, selected_order):
    total_value = 0
    num_batches, num_stages = matrix.shape

    for i in range(num_stages):
        batch_index = int(selected_order[i])
        total_value += matrix[batch_index, i]
    
    return total_value

def run_all_strats(matrix, v=None):
    """
    Основная функция для выполнения выбранной стратегии.
    matrix - квадратная матрица с партиями свеклы и этапами переработки.
    strategy - одна из стратегий: 'T', 'GT', 'TG'.
    v - если необходимо для стратегии GT или TG.
    """
    """ results = [G, T, GT, TG] """
    results = []
    
    final_value = Maximum(matrix)
    results.append(final_value)

    final_value = Minimum(matrix)
    results.append(final_value)

    final_value = thrifty_strategy(matrix)
    results.append(final_value)
    
    final_value = greedy_strategy(matrix)
    results.append(final_value)
    
    final_value = gt_strategy(matrix, v)
    results.append(final_value)
    
    final_value = tg_strategy(matrix, v)
    results.append(final_value)
    
    return results

def processing_run(data):
    n = data.get("num_parties")
    num_of_days_for_one_period = int((100/n + 0.5))
    v = n // 2 # Брать из UI

    a_min = data.get("a_min")
    a_max = data.get("a_max")

    beta1 = data.get("b_min")
    beta2 = data.get("b_max")

    distribution = data.get("distribution")
    if distribution == "концентрированное":
        distribution_type = 'c'
    elif distribution == "равномерное":
        distribution_type = 'u'

    ripening = data.get("need_ripening")

    inorganic_effects = data.get("inorganic_effects")

    res = [0, 0, 0, 0, 0, 0]
    for i in range(50):
        L = L_matrix.calculate_L_matrix(n, L_matrix.K_range, L_matrix.Na_range, L_matrix.N_range, L_matrix.I_range,num_of_days_for_one_period, inorganic_effects, ripening=True, v=v)
        delta_values = np.random.uniform(0, (beta2 - beta1) / 4, n)  # Генерация случайных delta_i
        L = L * 0.01
        B = generate_bij(n, beta1, beta2, distribution_type, delta_values, ripening, v)
        C = generate_c_matrix(a_min,a_max,B)
        S = C - L #this is condition matrix for further calculations

        # Вызов функции
        strats_results = run_all_strats(S, v)
        res = [x + y for x, y in zip(res, strats_results)]
    return [float(i) for i in strats_results]
