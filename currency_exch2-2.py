import requests
# import json
# import pprint
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb


def update_currency_label(event):
    code = target_combobox.get()
    name = currencies.get(code, '')
    currency_label.config(text=name)


def update_base_label(event):
    code = base_combobox.get()
    name = currencies.get(code, '')
    base_label.config(text=name)


def update_second_label(event):
    code = second_base_combobox.get()
    name = currencies.get(code, '')
    second_base_label.config(text=name)


def exchange():
    # code = entry.get().strip().upper()
    target_code = target_combobox.get()
    base_code = base_combobox.get()

    # Проверка на пустые поля, чтобы не вылетала ошибка
    if not target_code or not base_code:
        mb.showwarning('Предупреждение', 'Пожалуйста, выберите валюты')
        return

    if target_code and base_code:
        try:
            result = requests.get(f"https://open.er-api.com/v6/latest/{base_code}")
            result.raise_for_status()
            # data = json.loads(result.text)
            data = result.json()
            if target_code in data['rates']:
                exchange_rate = data['rates'][target_code]
                base = currencies[base_code]
                target = currencies[target_code]

                mb.showinfo('Курс обмена',
                            f'Курс '
                            f'  {exchange_rate:.1f}  {target} за 1 {base}')
            else:
                mb.showerror('Ошибка', f'Валюта {target_code} не найдена')


        except Exception as e:
            mb.showerror('Ошибка', f'error 400 {e}')


# result = requests.get("https://open.er-api.com/v6/latest/USD")
# data = json.loads(result.text)
# # print(data)
# # print(type(data))
# # for item in data.items():
# #     print(item)
# p = pprint.PrettyPrinter(indent=4)
# p.pprint(data)
currencies = {
    "USD": "Доллар США",
    "EUR": "Евро",
    "CNY": "Юань",
    "RUB": "Российский рубль",
}

pop_curr = ['EUR', 'USD', 'RUB', 'CNY']

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
button = Button(text='Получить курс обмена', width=25, height=1)
button.pack(pady=10)

# Привязка событий для обновления подписей
base_combobox.bind("<<ComboboxSelected>>", update_base_label)
second_base_combobox.bind("<<ComboboxSelected>>", update_second_label)
target_combobox.bind("<<ComboboxSelected>>", update_currency_label)

root.mainloop()