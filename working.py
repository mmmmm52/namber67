import json
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

class WeatherDiary:
    def __init__(self, master):
        self.master = master
        self.master.title("Weather Diary")
        self.records = []

        # Создаем интерфейс
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля для ввода
        tk.Label(self.master, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0)
        self.date_entry = tk.Entry(self.master)
        self.date_entry.grid(row=0, column=1)

        tk.Label(self.master, text="Температура (°C):").grid(row=1, column=0)
        self.temp_entry = tk.Entry(self.master)
        self.temp_entry.grid(row=1, column=1)

        tk.Label(self.master, text="Описание погоды:").grid(row=2, column=0)
        self.desc_entry = tk.Entry(self.master)
        self.desc_entry.grid(row=2, column=1)

        self.rain_var = tk.BooleanVar()
        tk.Checkbutton(self.master, text="Осадки", variable=self.rain_var).grid(row=3, column=1)

        # Кнопки
        tk.Button(self.master, text="Добавить запись", command=self.add_record).grid(row=4, column=0, pady=5)
        tk.Button(self.master, text="Сохранить в JSON", command=self.save_data).grid(row=4, column=1)
        tk.Button(self.master, text="Загрузить из JSON", command=self.load_data).grid(row=4, column=2)

        # Фильтрация
        tk.Label(self.master, text="Фильтр по дате (или оставьте пустым):").grid(row=5, column=0)
        self.filter_date_entry = tk.Entry(self.master)
        self.filter_date_entry.grid(row=5, column=1)
        tk.Button(self.master, text="Фильтровать по дате", command=self.filter_by_date).grid(row=5, column=2)

        tk.Label(self.master, text="Фильтр по температуре (>):").grid(row=6, column=0)
        self.filter_temp_entry = tk.Entry(self.master)
        self.filter_temp_entry.grid(row=6, column=1)
        tk.Button(self.master, text="Фильтровать по температуре", command=self.filter_by_temp).grid(row=6, column=2)

        # Таблица записей
        self.listbox = tk.Listbox(self.master, width=80)
        self.listbox.grid(row=7, column=0, columnspan=3, pady=10)

    def add_record(self):
        date_str = self.date_entry.get()
        temp_str = self.temp_entry.get()
        desc = self.desc_entry.get()

        # Проверка данных
        if not self.validate_date(date_str):
            messagebox.showerror("Ошибка", "Некорректный формат даты!")
            return
        if not self.validate_temperature(temp_str):
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return
        if not desc.strip():
            messagebox.showerror("Ошибка", "Описание не должно быть пустым!")
            return

        record = {
            "date": date_str,
            "temperature": float(temp_str),
            "description": desc,
            "precipitation": self.rain_var.get()
        }
        self.records.append(record)
        self.update_listbox()
        self.clear_entries()

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def validate_temperature(self, temp):
        try:
            float(temp)
            return True
        except ValueError:
            return False

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.rain_var.set(False)

    def update_listbox(self, filtered_records=None):
        self.listbox.delete(0, tk.END)
        records_to_show = filtered_records if filtered_records is not None else self.records
        for rec in records_to_show:
            rain_text = "Да" if rec["precipitation"] else "Нет"
            self.listbox.insert(tk.END, f"{rec['date']} | {rec['temperature']}°C | {rec['description']} | Осадки: {rain_text}")

    def save_data(self):
        with open("data.json", "w", encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists("data.json"):
            with open("data.json", "r", encoding='utf-8') as f:
                self.records = json.load(f)
            self.update_listbox()

    def filter_by_date(self):
        date_filter = self.filter_date_entry.get()
        if date_filter:
            filtered = [rec for rec in self.records if rec["date"] == date_filter]
            self.update_listbox(filtered_records=filtered)
        else:
            self.update_listbox()

    def filter_by_temp(self):
        temp_filter = self.filter_temp_entry.get()
        if temp_filter:
            try:
                temp_thresh = float(temp_filter)
                filtered = [rec for rec in self.records if rec["temperature"] > temp_thresh]
                self.update_listbox(filtered_records=filtered)
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение для температуры.")
        else:
            self.update_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
