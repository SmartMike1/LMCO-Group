from sqlalchemy import create_engine, text
from tkinter import *
from tksheet import Sheet
from tkinter import messagebox

import os
import sys
import shutil
import requests
import zipfile
import subprocess

# Функция создания пула соединений
def get_engine():
    conn_str = (
        "DRIVER={SQL Server};"
        # "SERVER=192.168.0.103, 1433;"
        # "SERVER=LAPTOP-2LTD9INR\SQLEXPRESS;"
        "SERVER=MIKE;"
        "DATABASE=Argentum1;"
        # "UID=Diplom;"
        # "PWD=My_Diplom_12345;"
    )
    return create_engine(
        f"mssql+pyodbc:///?odbc_connect={conn_str}",
        pool_size=20,        # Макс. одновременных соединений
        max_overflow=30,     # Доп. соединения при нагрузке
        pool_timeout=30,     # Время ожидания подключения
        pool_recycle=1800    # Переподключение каждые 30 минут
    )

# Функция обновления приложения
def update_version():
    try:
        version_url = "https://raw.githubusercontent.com/SmartMike1/LMCO-Group/refs/heads/main/version.txt"
        zip_url = "https://github.com/SmartMike1/LMCO-Group/archive/refs/heads/main.zip"
        zip_path = "update.zip"
        extract_path = "обновлённые_файлы"

        # Чтение текущей локальной версии из файла
        with open("version.txt", "r") as f: # , encoding="utf-8"
            current_version = f.read().strip()

        # Получение версии с GitHub
        response = requests.get(version_url)
        if response.status_code != 200:
            messagebox.showerror("Ошибка", "Не удалось получить версию с сервера.")
            return

        latest_version = response.text.strip()

        if latest_version == current_version:
            messagebox.showinfo("Информация", "Вы используете последнюю версию.")
            return

        confirm = messagebox.askyesno("Обновление", f"Доступна новая версия {latest_version}. Обновить?")
        if not confirm:
            return

        # Загрузка ZIP-архива
        with requests.get(zip_url, stream=True) as r:
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Распаковка
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Путь к корню распакованного архива
        repo_folder = os.path.join(extract_path, os.listdir(extract_path)[0])

        # Копирование файлов поверх текущего каталога
        for root, dirs, files in os.walk(repo_folder):
            rel_path = os.path.relpath(root, repo_folder)
            target_dir = os.path.join(os.getcwd(), rel_path)
            os.makedirs(target_dir, exist_ok=True)
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, file)
                shutil.copy2(src_file, dst_file)

        # Обновление хранимых процедур, если есть .sql-файлы
        update_sql_procedures(repo_folder)

        # Очистка временных файлов
        os.remove(zip_path)
        shutil.rmtree(extract_path)

        # Перезапуск приложения
        messagebox.showinfo("Готово", "Обновление установлено. Приложение будет перезапущено.")
        restart_program()

    except Exception as e:
        messagebox.showerror("Ошибка обновления", str(e))

# Функция перезапуска программы
def restart_program():
    if getattr(sys, 'frozen', False):
        # Если запущено как .exe
        exe_path = sys.executable
        subprocess.Popen([exe_path])
        sys.exit()
    else:
        # Если запущено как .py
        exe_path = sys.executable
        script_path = os.path.abspath(sys.argv[0])
        subprocess.Popen([exe_path, script_path])
        sys.exit()

# Функция обновления хранимых процедур
def update_sql_procedures(folder_path):
    sql_folder = os.path.join(folder_path, "sql")
    if not os.path.exists(sql_folder):
        return

    for filename in os.listdir(sql_folder):
        if filename.endswith(".sql"):
            file_path = os.path.join(sql_folder, filename)
            with open(file_path, 'r') as file: #, encoding="utf-8"
                sql_code = file.read()
            try:
                with engine.connect() as conn:
                    conn.execute(text(sql_code))
            except Exception as e:
                messagebox.showwarning("SQL ошибка", f"Ошибка в {filename}:\n{e}")

# Функция центрирования окон
def center_window(window, width, height, x, y):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x += (screen_width - width) // 2
    y += (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

# Получение данных для табличного отображения
def get_data_for_table(proc_name, max_len = 25):
    with engine.connect() as conn:
        result = conn.execute(text(proc_name))
        columns = list(result.keys())
        rows = []
        for row in result:
            prom_rows = []
            for data in row:
                if isinstance(data, str):
                    # Ищем первый пробел после max_len
                    space_index = data.find(' ', max_len)
                    if space_index != -1:
                        data = data[:space_index] + '\n' + data[space_index+1:]
                    else:
                        # Если пробела нет, просто делим по max_len
                        data = data[:max_len] + '\n' + data[max_len:]
                prom_rows.append(data)
            rows.append(prom_rows)
        
    return columns, rows

# Табличное отображение данных
def get_table(frame, proc_name, width):
    # Получение данных
    columns, rows = get_data_for_table(proc_name)

    # Установка заголовков
    sheet = Sheet(frame, headers=list(columns), data=rows,
                    show_x_scrollbar=True, show_y_scrollbar=True,
                    width=width)
        
    # Включение встроенных функций
    sheet.enable_bindings((
            "single_select",
            "column_select",
            "row_select",
            "arrowkeys",
            "row_height_resize",
            "column_width_resize",
            "column_select",
            "copy",
            "undo",
            "edit_cell"))
        
    # Отключение встроенных функций
    sheet.disable_bindings(["edit_cell", "paste", "delete"])

    # Считаем максимальную ширину каждого столбца и задаём её
    # max_data, max_len = max_string_length(rows)
    # print(max_data, "\n", max_len)
    # width_1_Sym = 5
    # max_width = max_string_length(rows)[1] * width_1_Sym
        
    for col in range(len(columns)):
        sheet.column_width(col, width=250)

    # Настройка высоты строк
    for row in range(len(rows)):
        sheet.row_height(row, height=50)

    sheet.pack(fill="both", expand=True)

    return sheet

# Получение данных для текстового отображения
def get_data_for_text(proc_name):
    with engine.connect() as conn:
        result = conn.execute(text(proc_name))
        columns = list(result.keys())
        rows = []
        for row in result:
            for data in row:
                if isinstance(data, str):
                    rows.append(data.strip())
                else:
                    rows.append(data)
        
    return columns, rows

# Максимальная длина строки в списке строк
def max_string_length(rows):
    max_len = 0
    max_data = ""
    for row in rows:
        for data in row:
            if isinstance(data, str):
                if data.startswith("https"):
                    continue
                elif max_len < len(data):
                    max_len = len(data)
                    max_data = data
    return max_data, max_len

# Функция изменения стиля Button
def styled_button(master, **kwargs):
    Default = {
    "bg": "#036fc7",
    "fg": "white",
    "font": ("Arial", 14),
    "relief": "solid",
    "borderwidth": 1,
    "activebackground": "#a0d0ff"
    }
    params = Default.copy()
    params.update(kwargs)
    return Button(master, **params)

# Функция изменения стиля Label
def styled_label(master, **kwargs):
    Default = {
    "bg": "white",
    "fg": "black",
    "font": ("Arial", 14)
    }
    params = Default.copy()
    params.update(kwargs)
    return Label(master, **params)

# Фукция установки белого фона всем дочерним элементам окна
def set_white_bg_recursive(widget):
    try:
        if isinstance(widget, (Button, Text, Entry)):
            return
        widget.configure(bg="white")
    except:
        pass
    for child in widget.winfo_children():
        set_white_bg_recursive(child)

# Изменение фона поля при фокусе в нём
def on_focus_in(event):
    event.widget.configure(bg="white")

# Установка эффекта нажатия кнопки
def on_key_press(event):
    event.widget.config(relief="sunken")

# Возврат нормального вида кнопки
def on_key_release(event):
    event.widget.config(relief="raised")
    event.widget.invoke()  # Вызвать действие

engine = get_engine()
