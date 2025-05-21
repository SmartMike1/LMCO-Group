import textwrap
import webbrowser
from Functions import *


from tkinter import *
from tkinter import messagebox, ttk
import tkinter.font as tkFont

from PIL import Image, ImageTk
from sqlalchemy import text


# Каркас инициализации окна
class BasedWindow(Toplevel):
    # x, y - некоторый сдвиг окна, чтобы окна не перекрывались
    # width=700
    def __init__(self, master, engine, title,
                width=750, height=500, x=0, y=0):
        super().__init__(master)
        self.master = master
        self.engine = engine
        self.title(title)
        self.font = ("Arial", 20)
        self.configure(bg="white")
        center_window(self, width, height, x, y)
        self.resizable(False, False)
        # self.resizable(True, True)

# Окно авторизации
class LoginWindow(BasedWindow):
    def __init__(self, master, engine):
        super().__init__(master, engine, title="Авторизация",
                        width=425, height=200)
        
        self.protocol("WM_DELETE_WINDOW", master.destroy)
        self.init_widgets()

    def init_widgets(self):
        LoginCanvas = Canvas(self, bg="white")
        LoginCanvas.pack(fill="both", expand=True)
        LoginCanvas.update() # Обновляем информацию о размерах окна

        label1 = styled_label(self, text="Логин:")
        self.login = Entry(self, font=self.font, background="lightgray")

        label2 = styled_label(self, text="Пароль:")
        self.password = Entry(self, show="*", font=self.font,
                            background="lightgray")

        button1 = styled_button(self, text="Войти", width=8,
                                command=self.try_login)
        button2 = styled_button(self, text="Обновить", width=8,
                                command=update_version)

        LoginCanvas.create_window(50, 50, window=label1)
        LoginCanvas.create_window(50, 100, window=label2)
        LoginCanvas.create_window(250, 50, window=self.login)
        LoginCanvas.create_window(250, 100, window=self.password)
        LoginCanvas.create_window(105, 150, anchor="nw", window=button1)
        LoginCanvas.create_window(225, 150, anchor="nw", window=button2)

        self.login.focus_set()
        self.login.bind("<FocusIn>", on_focus_in)
        self.password.bind("<FocusIn>", on_focus_in)
        button1.bind("<Button-1>", on_key_press)
        button1.bind("<Button-3>", on_key_press)
        button1.bind("<KeyPress-Return>", on_key_press)
        button1.bind("<KeyRelease-Return>", on_key_release)

        # Изменяем размер виджетов при изменении геометрической сетки
        for i in range(0,2):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)

    def try_login(self):
        login = self.login.get()
        password = self.password.get()

        try:
            with engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT COUNT(*) FROM Пользователи WHERE Имя=:u AND Пароль=:p"
                ), {'u': login, 'p': password})

                if result.scalar() == 1:
                    self.destroy()
                    app = Application(master=self.master, engine=engine, login=login)
                else:
                    messagebox.showerror("Ошибка", "Неверный логин или пароль")
        except Exception as e:
            messagebox.showerror("Ошибка подключения", str(e))
            self.master.destroy()

# Окно приложения
class Application(BasedWindow):
    # Инициализация окна
    def __init__(self, master=None, engine=None, login=None):
        super().__init__(master, engine, title="Аргентум")
        self.protocol("WM_DELETE_WINDOW", master.destroy)

        self.img = Image.open("images\Logo-LMCO.png")
        self.img = self.img.resize((300, 300))
        self.photo = ImageTk.PhotoImage(self.img)

        self.resizable(False, False)
        self.font = ("Arial", 20)
        self.login = login

        self.create_widgets()
        set_white_bg_recursive(self)

    # Начальное окно с кнопками действия
    def create_widgets(self):
        self.focus_force()
        self.MainCanvas = Canvas(self, bg="white")
        self.MainCanvas.pack(fill="both", expand=True)

        self.MainCanvas.update() # Обновляем информацию о размерах окна
        self.MainCanvas.create_image(420, 140,
                                image=self.photo, anchor="nw")
        
        text1 = "         Добро пожаловать!\n"
        text2 = "Выберите желаемое действие\n"
        itext = text1 + text2
        text3 = "Настройки Реактивов"

        # Кнопки действия для Реактивов font=("Arial", 16)
        self.button_1 = styled_button(self, text="Поиск", font=self.font,
                                    width=23, command=self.search_for)
        self.button_2 = styled_button(self, text="Добавление", font=self.font,
                                    width=10, command=self.add_new)
        self.button_3 = styled_button(self, text="Изменение", font=self.font,
                                    width=10, command=self.correct_Rinfo)
        self.button_4 = styled_button(self, text="Показать всё", font=self.font,
                                    width=23, command=self.read_all)
        self.button_5 = styled_button(self, text="Список покупок", font=self.font,
                                    width=23, bg="#69b900", command=self.order_list)
        self.button_6 = styled_button(self, text="Настройки Пользователей",
                                    font=self.font, width=23,
                                    command=self.user_settings)
        
        self.MainCanvas.create_text(200, 25, text=itext, font=self.font,
                                anchor="nw")
        self.MainCanvas.create_text(25, 100, text=text3, font=self.font,
                                anchor="nw")
        self.MainCanvas.create_window(25, 140, anchor="nw", window=self.button_1)
        self.MainCanvas.create_window(25, 200, anchor="nw", window=self.button_2)
        self.MainCanvas.create_window(233, 200, anchor="nw", window=self.button_3)
        self.MainCanvas.create_window(25, 260, anchor="nw", window=self.button_4)
        self.MainCanvas.create_window(25, 340, anchor="nw", window=self.button_5)
        self.MainCanvas.create_window(25, 400, anchor="nw", window=self.button_6)
    
    # Окно настроек Пользователей
    def user_settings(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Настройки пользователей", x=50, y=50)
        window.focus_force()
        wCanvas = Canvas(window, bg="white")
        wCanvas.pack(fill="both", expand=True)

        text1 = "Выберите желаемое действие"

        # Кнопки действия для Пользователей
        self.button_7 = styled_button(wCanvas, text="Поиск", font=self.font,
                                    width=23, command=self.search_for_user)
        self.button_8 = styled_button(wCanvas, text="Добавление", font=self.font,
                                    width=10, command=self.create_user)
        self.button_9 = styled_button(wCanvas, text="Изменение", font=self.font,
                                    width=10, command=self.correct_Uinfo)
        self.button_10 = styled_button(wCanvas, text="Показать всех", font=self.font,
                                    width=23, command=self.read_all_users)

        wCanvas.create_text(200, 25, text=text1, font=self.font,
                                anchor="nw")
        wCanvas.create_window(25, 100, anchor="nw", window=self.button_7)
        wCanvas.create_window(25, 160, anchor="nw", window=self.button_8)
        wCanvas.create_window(233, 160, anchor="nw", window=self.button_9)
        wCanvas.create_window(25, 220, anchor="nw", window=self.button_10)

    # Функции работы с Реактивами
    def read_all(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Просмотр всех Реактивов",
                        width=700, x=50, y=50)
        window.focus_force()

        # Контейнер для таблицы и прокрутки
        frame = Frame(window, bg="white")
        # frame.grid(row=0, column=0)
        frame.pack(fill="both", expand=True)

        # Отображаем данные
        get_table(frame, "ReadAllReagents", frame.winfo_width())

    def add_new(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Добавление нового Реактива",
                        width=620, x=50, y=50)
        window.focus_force()

        self.TableName = "Реагенты"
        self.OperationName = "INSERT"

        self.canvas = Canvas(window, width=600, height=300, bg="white")
        self.canvas.grid(row=0, column=0)
        canvas_frame = Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

        # Создаем Scrollbar и привязываем его к Canvas
        scrollbar = Scrollbar(window, bg="white", orient="vertical",
                                    command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.config(yscrollcommand=scrollbar.set)

        # Привязываем событие колесика мыши к прокрутке Canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        try:
            querry = f"CorrectReagentInformation '{1}'"
            columns, rows = get_data_for_text(querry)

            self.text_fields = []
            self.original_values = []
            self.column_names = []

            for index, col_name in enumerate(columns[1:]):
                label = styled_label(canvas_frame, text=col_name)
                label.grid(row=index, column=0, padx=5, pady=5)

                text_widget = Text(canvas_frame, width=50, height=2,
                                    font=self.font, wrap=WORD)
                text_widget.grid(row=index, column=1, padx=5, pady=5)
                # text_widget.insert(1.0, rows[index])

                self.text_fields.append(text_widget)
                self.original_values.append(rows[index])
                self.column_names.append(col_name)

            # Обновляем, чтобы прокрутка работала правильно
            canvas_frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            button = styled_button(window, text="Сохранить Информацию",
                            command=self.insert_changes)
            button.grid(row=2, column=0, sticky="we", padx=10, pady=10)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить процедуру:\n{e}")
        set_white_bg_recursive(self)

    # !!! НЕДОПИСАНО !!!
    def insert_changes(self):
        changes = {}

        for i, text_widget in enumerate(self.text_fields):
            new_value = text_widget.get("1.0", END).strip()
            old_value = self.original_values[i].strip()

            if new_value != old_value:
                changes[self.column_names[i]] = (old_value, new_value)

        if not changes:
            messagebox.showinfo("Информация", "Нет информации для вставки.")
            return
        
        try:
            insert = text("ProcUpdateField :id, :field, :value")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить процедуру:\n{e}")
    # !!! НЕДОПИСАНО !!!

    def search_for(self):
        self.window = BasedWindow(master=self.master, engine=engine,
                        title="Поиск Реактива", x=50, y=50)
        
        self.window.focus_force()
        
        self.window.update()
        self.form = Frame(self.window, width=self.window.winfo_width(), bg="white")
        self.form.grid(row=0, column=0, columnspan=3, sticky="snwe",
                        padx=10, pady=10)

        label = styled_label(self.form, text="Введите номер реактива:")
        label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.number = Entry(self.form, font=self.font, background="lightgray")
        self.number.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        button = styled_button(self.form, text="Найти", command=self.search)
        button.grid(row=0, column=2, sticky="w", padx=10, pady=10)

        self.form2 = Frame(self.window, width=self.window.winfo_width(), bg="white")
        self.form2.grid(row=1, column=0, columnspan=3, sticky="snwe",
                        padx=10, pady=10)
        
        self.number.bind("<FocusIn>", on_focus_in)

    def search(self):
        number = self.number.get()
        # print(number)
        # Удаляем старые виджеты из контейнера (если есть)
        for widget in self.form2.winfo_children():
            widget.destroy()
        
        # Отображаем данные
        get_table(self.form2, f"SearchReagent '{number}'",
                    self.window.winfo_width() - 25)
        
    def correct_Rinfo(self):
        self.Cwindow = BasedWindow(master=self.master, engine=engine,
                title="Изменение данных по Реактиву",
                x=50, y=50) # width=620, height=450,

        self.Cwindow.update()
        self.Cwindow.focus_force()

        self.TableName = "Реагенты"
        self.OperationName = "UPDATE"

        # Создаем Canvas
        self.canvas = Canvas(self.Cwindow, width=680, height=350, bg="white")
        self.canvas.grid(row=1, column=0)

        # Создаем Scrollbar и привязываем его к Canvas
        self.scrollbar = Scrollbar(self.Cwindow, orient="vertical",
                                    command=self.canvas.yview, bg="white")
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Привязываем событие колесика мыши к прокрутке Canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Создаем Frame внутри Canvas для размещения содержимого
        self.canvas_frame = Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        self.form = Frame(self.Cwindow, bg="white")
        self.form.grid(row=0, column=0, columnspan=3, sticky="snwe",
                        padx=10, pady=10)

        label = styled_label(self.form, text="Введите номер реактива:")
        label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.number = Entry(self.form, font=self.font, background="lightgray")
        self.number.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        button = styled_button(self.form, text="Найти", command=self.choose)
        button.grid(row=0, column=2, sticky="w", padx=10, pady=10)

        self.number.bind("<FocusIn>", on_focus_in)
        button.bind("<Return>")

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        # self.canvas1.yview_scroll(-1 * (event.delta // 120), "units")

    def choose(self):
        self.focus_force()
        self.window = BasedWindow(master=self.master, engine=engine,
                title="Выбор нужного Реактива",
                width=620, x=50, y=50)

        number = self.number.get()
        # Отображаем данные
        self.sheet = get_table(self.window, f"SearchReagent '{number}'",
                                self.window.winfo_width() - 25)

        self.sheet.enable_bindings(("cell_select", "double_click"))
        self.sheet.bind("<Double-Button-1>", self.on_sheet_double_click)

    def on_sheet_double_click(self, event):
        self.Cwindow.focus_force()
        # Удаляем старые виджеты из контейнера (если есть)
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        row_index = self.sheet.get_currently_selected()[0]
        if row_index is None:
            return

        row_values = self.sheet.get_row_data(row_index)
        self.reagent_id = row_values[0]

        try:
            querry = f"CorrectReagentInformation '{self.reagent_id}'"
            columns, rows = get_data_for_text(querry)

            self.text_fields = []
            self.original_values = []
            self.column_names = []

            for index, col_name in enumerate(columns):
                label = styled_label(self.canvas_frame, text=col_name)
                label.grid(row=index, column=0, padx=5, pady=5)

                if col_name == "КороткоеНазваниеЕдИзм":
                    querryM = f"AllMeasures"
                    columnsM, rowsM = get_data_for_text(querryM)

                    box_widget = ttk.Combobox(self.canvas_frame, values=rowsM,
                                                state="readonly", font=self.font,
                                                width=34)
                    box_widget.grid(row=index, column=1, padx=5, pady=5)
                    box_widget.set("Выберите единицу...")
                elif col_name == "СтатусРеагента":
                    querryS = f"AllStatus"
                    columns, rowsS = get_data_for_text(querryS)

                    box_widget = ttk.Combobox(self.canvas_frame, values=rowsS,
                                                state="readonly", font=self.font,
                                                width=34)
                    box_widget.grid(row=index, column=1, padx=5, pady=5)
                    box_widget.set("Выберите статус...")
                else:
                    text_widget = Text(self.canvas_frame, width=35, height=2,
                                    font=self.font, relief="solid", wrap=WORD)
                    text_widget.grid(row=index, column=1, padx=5, pady=5)
                    text_widget.insert(1.0, rows[index])

                    self.text_fields.append(text_widget)
                    self.original_values.append(rows[index])
                    self.column_names.append(col_name)

            # Обновляем, чтобы прокрутка работала правильно
            self.canvas_frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            # Закрываем окно "Выбор нужного Реактива"
            self.window.destroy()

            button = styled_button(self.Cwindow, text="Сохранить Информацию",
                            command=self.update_changes)
            button.grid(row=2, column=0, sticky="we", padx=10, pady=10)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить процедуру:\n{e}")
    
    def update_changes(self):
        changes = {}

        for i, text_widget in enumerate(self.text_fields):
            new_value = text_widget.get("1.0", END).strip()
            old_value = self.original_values[i].strip()

            if new_value != old_value:
                changes[self.column_names[i]] = (old_value, new_value)

        if not changes:
            messagebox.showinfo("Информация", "Нет изменений для сохранения.")
            return
        
        try:
            update   = text("ProcUpdateField :id, :field, :value")
            user     = text("GetUserIdBySurname :surname")
            log_proc = text("LogChange :user_id, :table_name, :operation, :field, :before, :after")

            for column, (old, new) in changes.items():
                with engine.connect() as conn:
                    # Определяем ID по Фамилии
                    result = conn.execute(user, {"surname": self.login}).fetchone()
                    user_id = result[0]

                    # Изменяем данные Реагента
                    conn.execute(update, {"id": self.reagent_id, "field": column, "value": new})

                    # Логируем изменения
                    conn.execute(log_proc, {"user_id": user_id, "table_name": self.TableName,
                                            "operation": self.OperationName, "field": column,
                                            "before": old, "after": new})
                    conn.commit()

            messagebox.showinfo("Успех", "Изменения успешно сохранены.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить изменения:\n{e}")

    def order_list(self):
        pass
    # !!!!!!! Не написано !!!!!!!
    def delete_reagent(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Списание Реактива",
                        width=620, x=50, y=50)
    # !!!!!!! Не написано !!!!!!!

    # Функции работы с Пользователями
    # !!!!!!! Не написано !!!!!!!
    def read_all_users(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Просмотр всех пользователей",
                        width=620, x=50, y=50)
        window.focus_force()

        self.TableName = "Пользователи"
    # !!!!!!! Не написано !!!!!!!
    def create_user(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Добавление пользователя",
                        width=620, x=50, y=50)
        window.focus_force()

        self.TableName = "Пользователи"
    # !!!!!!! Не написано !!!!!!!
    def search_for_user(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Просмотр всех пользователей",
                        width=620, x=50, y=50)
        window.focus_force()

        self.TableName = "Пользователи"
    # !!!!!!! Не написано !!!!!!!
    def correct_Uinfo(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Изменение информации о пользователе",
                        width=620, x=50, y=50)
        window.focus_force()

        self.TableName = "Пользователи"
    # !!!!!!! Не написано !!!!!!!
    def delete_user(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Удаление пользователя",
                        width=620, x=50, y=50)
        window.focus_force()

        self.TableName = "Пользователи"
    # !!!!!!! Не написано !!!!!!!

    # !!!!!!! Не написано !!!!!!!
    def order_list(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Формирование списка заказа",
                        width=620, x=50, y=50)
    # !!!!!!! Не написано !!!!!!!

# Запускаемся
if __name__ == "__main__":
    # engine = get_engine()

    root = Tk()
    root.withdraw()
    login = LoginWindow(master=root, engine=engine)

    login.mainloop()
