from tkinter import messagebox

def toggle_ripening(obj):
    """Переключение видимости полей для дозаривания."""
    if obj.need_ripening_var.get():
        obj.ripening_frame.pack(fill='x', pady=5, padx=10, after=obj.need_ripening_checkbutton)
    else:
        obj.ripening_frame.pack_forget()

def validate_data(obj):
    """Получение данных из полей и валидация."""
    try:
        # Сбор данных в словарь
        data = {}

        num_parties = int(obj.parties_entry.get())
        if not(num_parties > 0):
            raise ValueError("Количество партий должно быть положительно.")
        data["num_parties"] = num_parties

        a_min = float(obj.a_min_entry.get())
        a_max = float(obj.a_max_entry.get())
        if not(a_min < a_max and 0.12 <= a_min <= 0.22 and 0.12 <= a_min <= 0.22):
            raise ValueError("a_min должен быть меньше a_max\nпринадлежат [0.12,0.22]")
        data["a_min"] = a_min
        data["a_max"] = a_max

        distribution = obj.distribution_combobox.get()
        if distribution not in ("равномерное", "концентрированное"):
            raise ValueError("Выберите корректное распределение.")
        data["distribution"] = distribution

        b_min = float(obj.b_min_entry.get())
        b_max = float(obj.b_max_entry.get())
        if not(b_min < b_max and 0.85 < b_min < 1 and 0.85 < b_max < 1):
            raise ValueError("b_min должен быть меньше b_max\nпринадлежат [0.12,0.22]")
        data["b_min"] = b_min
        data["b_max"] = b_max

        need_ripening = obj.need_ripening_var.get()
        data["need_ripening"] = need_ripening
        if need_ripening:
            r_min = float(obj.ripening_min_entry.get())
            r_max = float(obj.ripening_max_entry.get())
            if not(r_min < r_max and 1 < r_min < 1.15 and 1 < r_max < 1.15):
                raise ValueError("Коэффициенты дозаривания заданы некорректно.")
            data["r_min"] = r_min
            data["r_max"] = r_max
            transition_number = int(obj.transition_entry.get())
            if not(2 <= transition_number <= num_parties):
                raise ValueError("Номер перехода от дозаривания к деградированию некорректно.")
            data["transition_number"] = transition_number
        else:
            data["r_min"] = None
            data["r_max"] = None
            data["transition_number"] = None

        inorganic_effects = obj.inorganic_effects_var.get()
        data["inorganic_effects"] = inorganic_effects

        # Возврат словаря с данными
        return data
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Ошибка ввода данных: {e}")
