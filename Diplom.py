import textwrap
import webbrowser
from Functions import *


from tkinter import *
from tkinter import messagebox, ttk

from PIL import Image, ImageTk
from sqlalchemy import text


# Каркас инициализации окна
class BasedWindow(Toplevel):
    # x, y - некоторый сдвиг окна, чтобы окна не перекрывались
    def __init__(self, master, engine, title,
                width=600, height=400, x=0, y=0):
        super().__init__(master)
        self.master = master
        self.engine = engine
        self.title(title)
        center_window(self, width, height, x, y)
        # self.resizable(False, False)
        self.resizable(True, True)

# Окно авторизации
class LoginWindow(BasedWindow):
    def __init__(self, master, engine):
        super().__init__(master, engine, title="Авторизация",
                        width=350, height=200)
        
        self.font = ("Arial", 14)
        self.protocol("WM_DELETE_WINDOW", master.destroy)
        self.init_widgets()

    def init_widgets(self):
        label1 = Label(self, text="Логин:", font=self.font)
        label1.grid(row=0, column=0, sticky="e", padx=5)
        self.login = Entry(self, font=self.font, background="lightgray")
        self.login.grid(row=0, column=1, sticky="w", padx=5)

        label2 = Label(self, text="Пароль:", font=self.font)
        label2.grid(row=1, column=0, sticky="e", padx=5)
        self.password = Entry(self, show="*", font=self.font, background="lightgray")
        self.password.grid(row=1, column=1, sticky="w", padx=5)

        button1 = styled_button(self, text="Войти", command=self.try_login)
        button1.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        button2 = styled_button(self, text="Обновить", command=update_version)
        button2.grid(row=2, column=0, sticky="w", padx=10, pady=10)

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
        super().__init__(master, engine, title="Аргентум",
                        width=600, height=400)
        self.protocol("WM_DELETE_WINDOW", master.destroy)

        self.img = Image.open("images\Logo-LMCO.png")
        self.img = self.img.resize((75, 75))
        self.photo = ImageTk.PhotoImage(self.img)

        self.resizable(False, False)
        self.font = ("Arial", 14)
        self.login = login

        self.create_widgets()

    # Начальное окно с кнопками действия
    def create_widgets(self):
        self.focus_force()
        self.canvas = Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        self.update() # Обновляем информацию о размерах окна
        self.canvas.create_image(self.winfo_width() - self.img.size[0], 0,
                                image=self.photo, anchor="nw")
        
        text1 = "         Добро пожаловать!\n"
        text2 = "Выберите желаемое действие\n"
        itext = text1 + text2
        self.canvas.create_text(25, 25, text=itext, font=("Arial", 18),
                                anchor="nw")

        self.button_1 = styled_button(self, text="Просмотр Всех Реактивов",
                                    command=self.read_all)
        self.button_2 = styled_button(self, text="Добавление нового Реактива",
                                    command=self.add_new)
        self.button_3 = styled_button(self, text="Поиск Реактивов",
                                    command=self.search_for)
        self.button_4 = styled_button(self, text="Изменение данных по Реактиву",
                                    command=self.correct_reagent)
        
        self.canvas.create_window(25, 100, anchor="nw", window=self.button_1)
        self.canvas.create_window(25, 150, anchor="nw", window=self.button_2)
        self.canvas.create_window(25, 200, anchor="nw", window=self.button_3)
        self.canvas.create_window(25, 250, anchor="nw", window=self.button_4)
    
    def read_all(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Просмотр всех Реактивов",
                        width=700, x=50, y=50)
        window.focus_force()

        # Контейнер для таблицы и прокрутки
        frame = Frame(window)
        # frame.grid(row=0, column=0)
        frame.pack(fill="both", expand=True)

        # Отображаем данные
        get_table(frame, "ReadAllReagents", frame.winfo_width())

    # !!!!!!! Не написано !!!!!!!
    def add_new(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Добавление нового Реактива",
                        width=620, x=50, y=50)
    # !!!!!!! Не написано !!!!!!!

    def search_for(self):
        self.window = BasedWindow(master=self.master, engine=engine,
                        title="Поиск Реактива", x=50, y=50)
        
        self.window.focus_force()
        
        self.window.update()
        self.form = Frame(self.window, width=self.window.winfo_width())
        self.form.grid(row=0, column=0, columnspan=3, sticky="snwe",
                        padx=10, pady=10)

        label = Label(self.form, text="Введите номер реактива:",
                        font=self.font)
        label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.number = Entry(self.form, font=self.font, background="lightgray")
        self.number.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        button = styled_button(self.form, text="Найти", command=self.search)
        button.grid(row=0, column=2, sticky="w", padx=10, pady=10)

        self.form2 = Frame(self.window, width=self.window.winfo_width())
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
        
    def correct_reagent(self):
        self.Cwindow = BasedWindow(master=self.master, engine=engine,
                title="Изменение данных по Реактиву",
                width=620, height=450, x=50, y=50)

        self.Cwindow.update()
        self.Cwindow.focus_force()

        # Создаем Canvas
        self.canvas = Canvas(self.Cwindow, width=600, height=300)
        self.canvas.grid(row=1, column=0)

        # Создаем Scrollbar и привязываем его к Canvas
        self.scrollbar = Scrollbar(self.Cwindow, orient="vertical",
                                    command=self.canvas.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Привязываем событие колесика мыши к прокрутке Canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Создаем Frame внутри Canvas для размещения содержимого
        self.canvas_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        self.form = Frame(self.Cwindow)
        self.form.grid(row=0, column=0, columnspan=3, sticky="snwe",
                        padx=10, pady=10)

        label = Label(self.form, text="Введите номер реактива:", font=self.font)
        label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.number = Entry(self.form, font=self.font, background="lightgray")
        self.number.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        button = styled_button(self.form, text="Найти", command=self.choose)
        button.grid(row=0, column=2, sticky="w", padx=10, pady=10)

        self.number.bind("<FocusIn>", on_focus_in)
        button.bind("<Return>")

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

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

            for index, col_name in enumerate(columns[1:]):
                label = Label(self.canvas_frame, text=col_name, font=self.font)
                label.grid(row=index, column=0, padx=5, pady=5)

                text_widget = Text(self.canvas_frame, width=50, height=2,
                                    font=self.font, wrap=WORD)
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
                            command=self.save_changes)
            button.grid(row=2, column=0, sticky="we", padx=10, pady=10)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить процедуру:\n{e}")
    
    def save_changes(self):
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
            query = text("ProcUpdateField :id, :field, :value")
            user  = text("GetUserIdBySurname :surname")
            log_proc = text("LogChange :user_id, :table_name, :operation, :field, :before, :after")

            for column, (old, new) in changes.items():
                with engine.connect() as conn:
                    # Определяем ID по Фамилии
                    result = conn.execute(user, {"surname": self.login}).fetchone()
                    user_id = result[0]

                    # Изменяем данные Реагента
                    conn.execute(query, {"id": self.reagent_id, "field": column, "value": new})

                    # Логируем изменения
                    conn.execute(log_proc, {"user_id": user_id, "table_name": "Реагенты",
                                            "operation": "UPDATE", "field": column,
                                            "before": old, "after": new})
                    conn.commit()

            messagebox.showinfo("Успех", "Изменения успешно сохранены.")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить изменения:\n{e}")

    # !!!!!!! Не написано !!!!!!!
    def delete_reagent(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Списание Реактива",
                        width=620, x=50, y=50)
    # !!!!!!! Не написано !!!!!!!

    # !!!!!!! Не написано !!!!!!!
    def create_user(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Добавление пользователя",
                        width=620, x=50, y=50)
    # !!!!!!! Не написано !!!!!!!

    # !!!!!!! Не написано !!!!!!!
    def delete_user(self):
        window = BasedWindow(master=self.master, engine=engine,
                        title="Удаление пользователя",
                        width=620, x=50, y=50)
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
