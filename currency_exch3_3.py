import requests

# Создаем графический интерфейса
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb


# Название валюты под полем выбора целевой валюты
def update_currency_label(event):
    code = target_combobox.get()
    name = currencies.get(code, '')
    currency_label.config(text=name)


# Название валюты под полем выбора базовой валюты
def update_base_label(event):
    code = base_combobox.get()
    name = currencies.get(code, '')
    base_label.config(text=name)


# Назваеие валюты под полем выбора второй базовой валюты
def update_second_label(event):
    code = second_base_combobox.get()
    name = currencies.get(code, '')
    second_base_label.config(text=name)


# Запрос курса одной валюты к другой через API и возвращает значение
def get_rate(base_code, target_code):
    result = requests.get(f"https://open.er-api.com/v6/latest/{base_code}")
    result.raise_for_status()
    data = result.json()
    if target_code in data['rates']:
        return data['rates'][target_code]
    return None


# Обработка нажатия кнопки: получает и показывает курсы обеих базовых валют к целевой
def exchange():
    target_code = target_combobox.get()
    base_code = base_combobox.get()
    second_code = second_base_combobox.get()


    try:
        rate1 = get_rate(base_code, target_code)
        rate2 = get_rate(second_code, target_code)

        if rate1 is None:
            mb.showerror('Ошибка', f'Валюта {target_code} не найдена для {base_code}')
            return
        if rate2 is None:
            mb.showerror('Ошибка', f'Валюта {target_code} не найдена для {second_code}')
            return

        base1 = currencies[base_code]
        base2 = currencies[second_code]
        target = currencies[target_code]

        mb.showinfo('Курс обмена',
                    f'Курс  {rate1:.1f}  {target} за 1 {base1}\n'
                    f'Курс  {rate2:.1f}  {target} за 1 {base2}')

    except Exception as e:
        mb.showerror('Ошибка', f'error 400 {e}')




# Словарь соответствия кодов валют и их названий на русском
currencies = {
    "USD": "Доллар США",
    "EUR": "Евро",
    "CNY": "Юань",
    "RUB": "Российский рубль",
}

pop_curr = ['EUR', 'USD', 'RUB', 'CNY']

# Создание главного окна приложения
root = Tk()
root.title("Курсы обмена валют")
root.geometry("300x450")
root.resizable(False, False)

# Базовая валюта
Label(text='Базовая валюта', font=('Arial', 10, 'bold')).pack(pady=(15, 5))
base_combobox = ttk.Combobox(values=list(currencies.keys()), width=25)
base_combobox.pack()
base_label = Label(text='')
base_label.pack(pady=(0, 15))

# Вторая базовая валюта
Label(text='Вторая базовая валюта', font=('Arial', 10, 'bold')).pack(pady=(10, 5))
second_base_combobox = ttk.Combobox(values=list(currencies.keys()), width=25)
second_base_combobox.pack()
second_base_label = Label(text='')
second_base_label.pack(pady=(0, 15))

# Целевая валюта
Label(text='Целевая валюта', font=('Arial', 10, 'bold')).pack(pady=(10, 5))
target_combobox = ttk.Combobox(values=list(currencies.keys()), width=25)
target_combobox.pack()
currency_label = Label(text='')
currency_label.pack(pady=(0, 20))

# Кнопка
button = Button(text='Получить курс обмена', width=25, height=1, command=exchange)
button.pack(pady=10)

# Привязка событий для обновления подписей
base_combobox.bind("<<ComboboxSelected>>", update_base_label)
second_base_combobox.bind("<<ComboboxSelected>>", update_second_label)
target_combobox.bind("<<ComboboxSelected>>", update_currency_label)

# Запуск главного цикла обработки событий окна
root.mainloop()