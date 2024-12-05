import matplotlib.pyplot as plt
import tkinter as tk
def show_histogram(results_data):
    # Фиктивные данные
    heights = results_data  # Захардкоженные значения высоты столбцов
    labels = ["Max", "Min", "Greedy", "Thritty", "GT", "TG"]

    # Создание гистограммы
    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, heights, color=["blue", "orange", "green", "red"])
    plt.title("Результаты алгоритмов")
    plt.xlabel("Алгоритмы")
    plt.ylabel("Процент содержания сахара")
    plt.ylim(0.5, 4)

    for bar in bars:
        yval = bar.get_height()  # Высота столбика
        xval = bar.get_x() + bar.get_width() / 2  # X-координата центра столбика
        
        # Добавление текста с округлением высоты столбика до 2 знаков после запятой
        plt.text(xval, yval + 0.05, f'{yval:.4f}', ha='center', va='bottom', fontsize=10)

    plt.show()

