import numpy as np
def calculate_L_matrix(n, K_range, Na_range, N_range, I_range,num_of_days_for_one_period,organics, ripening=True,v=None):
    """
    Функция для вычисления матрицы потерь сахара с учетом влияния неорганических веществ.
    
    n - количество партий
    K_range, Na_range, N_range, I_range - диапазоны для K, Na, N, I
    ripening - флаг дозаривания
    v - количество этапов дозаривания
    """

    L = np.zeros((n, n))
    if (not organics):
        return L
    for i in range(n):
        # Случайная генерация значений для каждой партии
        K = np.random.uniform(K_range[0], K_range[1])
        Na = np.random.uniform(Na_range[0], Na_range[1])
        N = np.random.uniform(N_range[0], N_range[1])
        I0 = np.random.uniform(I_range[0], I_range[1])

        # Расчет содержания редуцирующих веществ для каждого этапа
        for j in range(n):
            I = I0 * (1.029)**(num_of_days_for_one_period * (j + 1 - num_of_days_for_one_period))
            Cx_M = 0.1541 * (K + Na) + 0.2159 * N + 0.9989 * I + 0.1967

            # Если дозаривание, то учитывать его влияние
            if ripening and j < v:
                L[i, j] = Cx_M  # Потери сахара при дозаривании
            else:
                L[i, j] = Cx_M  # Потери сахара без дозаривания
                
    return L

# Параметры диапазонов для каждого компонента
K_range = [4.8, 7.05]  # Диапазон для калия
Na_range = [0.21, 0.82]  # Диапазон для натрия
N_range = [1.58, 2.8]  # Диапазон для аминного азота
I_range = [0.62, 0.64]  # Диапазон для редуцирующих веществ



