import tkinter as tk
from tkinter import ttk, messagebox
from test_gui_methods import toggle_ripening, validate_data
from T_G_TG_GT import processing_run
from histogram import show_histogram

class SugarOptimizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Оптимизация выработки сахара")
        self.root.geometry("400x550")

        # Инициализация переменных
        self.need_ripening_var = tk.BooleanVar()
        self.inorganic_effects_var = tk.BooleanVar()

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        """Создает виджеты интерфейса."""
        # Поле для ввода количества партий
        ttk.Label(self.root, text="Количество партий:").pack(anchor='w', padx=10, pady=5)
        self.parties_entry = ttk.Entry(self.root)
        self.parties_entry.pack(fill='x', padx=10)

        # Поля для ввода a_min и a_max
        ttk.Label(self.root, text="Начальное содержание сахара (a_min, a_max) [0.12, 0.22]:").pack(anchor='w', padx=10, pady=5)
        self.a_min_entry = ttk.Entry(self.root)
        self.a_max_entry = ttk.Entry(self.root)
        self.a_min_entry.pack(fill='x', padx=10, pady=2)
        self.a_max_entry.pack(fill='x', padx=10, pady=2)

        # Выпадающий список распределения коэффициентов деградирования
        ttk.Label(self.root, text="Распределение коэффициентов деградирования:").pack(anchor='w', padx=10, pady=5)
        self.distribution_combobox = ttk.Combobox(self.root, values=["равномерное", "концентрированное"])
        self.distribution_combobox.pack(fill='x', padx=10)
        self.distribution_combobox.current(0)

        # Поля для ввода b_min и b_max
        ttk.Label(self.root, text="Коэффициенты деградирования (b_min, b_max) (0.85, 1):").pack(anchor='w', padx=10, pady=5)
        self.b_min_entry = ttk.Entry(self.root)
        self.b_max_entry = ttk.Entry(self.root)
        self.b_min_entry.pack(fill='x', padx=10, pady=2)
        self.b_max_entry.pack(fill='x', padx=10, pady=2)

        # Чекбокс "нужно ли дозаривание" и связанные с ним поля
        self.need_ripening_checkbutton = ttk.Checkbutton(
            self.root,
            text="Нужно ли дозаривание?",
            variable=self.need_ripening_var,
            command=lambda: self.toggle_ripening_fields()
        )
        self.need_ripening_checkbutton.pack(anchor='w', padx=10, pady=5)

        self.ripening_frame = ttk.Frame(self.root)
        ttk.Label(self.ripening_frame, text="Промежуток коэффициентов дозаривания (min, max) (1, 1.15):").pack(anchor='w', padx=10, pady=5)
        self.ripening_min_entry = ttk.Entry(self.ripening_frame)
        self.ripening_max_entry = ttk.Entry(self.ripening_frame)
        self.ripening_min_entry.pack(fill='x', padx=10, pady=2)
        self.ripening_max_entry.pack(fill='x', padx=10, pady=2)

        ttk.Label(self.ripening_frame, text="Номер перехода (2, N / 2):").pack(anchor='w', padx=10, pady=5)
        self.transition_entry = ttk.Entry(self.ripening_frame)
        self.transition_entry.pack(fill='x', padx=10, pady=2)

        # Чекбокс "Учитываем эффекты неорганических элементов"
        self.inorganic_effects_checkbutton = ttk.Checkbutton(
            self.root,
            text="Учитываем эффекты неорганических элементов",
            variable=self.inorganic_effects_var
        )
        self.inorganic_effects_checkbutton.pack(anchor='w', padx=10, pady=5)

        # Кнопка "Рассчитать"
        self.calculate_button = ttk.Button(self.root, text="Рассчитать", command=lambda: self.validate_and_process_data())
        self.calculate_button.pack(pady=10)

    def toggle_ripening_fields(self):
        """Переключение видимости полей для дозаривания."""
        toggle_ripening(self)

    def validate_and_process_data(self):
        """Получение данных из полей и валидация."""
        data = validate_data(self)
        if data is not None:
            # Вывод данных или дальнейшая обработка
            print(data)
            results = processing_run(data)
            show_histogram(results)
            print(results)
            
if __name__ == "__main__":
    root = tk.Tk()
    app = SugarOptimizationApp(root)
    root.mainloop()
