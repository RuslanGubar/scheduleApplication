import tkinter as tk
from tkinter import messagebox, Canvas, Label
import sqlite3
import time
import threading
from tkinter import ttk


def connect_db(db_file='phone_app.db'):
    """Подключается к базе данных."""
    conn = sqlite3.connect(db_file)
    return conn


def create_tables(conn):
    """Создает таблицы в базе данных."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            day TEXT,
            o_pair TEXT,
            t_pair TEXT,
            th_pair TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    # Добавлуние пользователей и расписания
    #cursor.execute("INSERT INTO users VALUES ('1', 'varus', '123456')")
    #cursor.execute("INSERT INTO users VALUES ('2', 'aaaa', '1111')")
    #cursor.execute("INSERT INTO schedule VALUES ('1', '1', 'пн', '-', 'Информатика ауд.254', 'Ангийский ауд.312')")
    #cursor.execute("INSERT INTO schedule VALUES ('2', '1', 'вт', '-', 'Русский ауд.225', 'Математика ауд. 385')")
    #cursor.execute("INSERT INTO schedule VALUES ('3', '1', 'ср', 'Русский ауд.225', 'Математика ауд. 385', 'География ауд.455')")
    #cursor.execute("INSERT INTO schedule VALUES ('4', '1', 'чт', 'Русский ауд.225', 'История ауд.215', '-')")
    #cursor.execute("INSERT INTO schedule VALUES ('5', '1', 'пт', 'Математика ауд. 385', 'История ауд.215', '-')")
    #cursor.execute("INSERT INTO schedule VALUES ('6', '1', 'сб', 'Математика ауд. 385', 'Русский ауд.225', '-')")
    #cursor.execute("INSERT INTO schedule VALUES ('7', '2', 'пн', 'Русский ауд.225', 'Ангийский ауд.312', '-')")
    #cursor.execute("INSERT INTO schedule VALUES ('8', '2', 'вт', 'Русский ауд.225', 'География ауд.455', 'История ауд.215')")
    #cursor.execute("INSERT INTO schedule VALUES ('9', '2', 'ср', 'Математика ауд. 385', 'Русский ауд.225', '-')")
    #cursor.execute("INSERT INTO schedule VALUES ('10', '2', 'чт', 'Математика ауд. 385', 'Русский ауд.225', '-')")
    #cursor.execute("INSERT INTO schedule VALUES ('11', '2', 'пт', 'Математика ауд. 385', 'Информатика ауд.254', '-')")
    #cursor.execute("INSERT INTO schedule VALUES ('12', '2', 'сб', 'Русский ауд.225', 'Математика ауд. 385', 'Информатика ауд.254')")

    conn.commit()
    conn.close()

class LoginWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Авторизация")
        self.geometry('350x500')

        self.username_label = tk.Label(self, text="Логин:", font=("Arial Bold", 20))
        self.username_label.grid(row=0, column=0, padx=50, pady=50)

        self.username_entry = tk.Entry(self, width=20)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self, text="Пароль:", font=("Arial Bold", 20))
        self.password_label.grid(row=1, column=0, padx=10, pady=10)

        self.password_entry = tk.Entry(self, width=20, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = tk.Button(self, text="Войти", command=self.login, font=("Arial Bold", 25), bg="springgreen1")
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.error_label = tk.Label(self, text="", fg="red", font=("Arial Bold", 10))
        self.error_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.error_label.config(text="")
            self.destroy()
            GreetingWindow(user[0]).mainloop()
        else:
            self.error_label.config(text="Ошибка авторизации")


class GreetingWindow(tk.Tk):
    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Приветствие")
        self.geometry('350x500')
        self.user_id = user_id
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id=?", (user_id,))
        username = cursor.fetchone()[0]
        conn.close()

        self.label = Label(self, text=f"Здравствуйте, {username}!", font=("Arial", 20))
        self.label.pack(pady=20)

        self.canvas = Canvas(self, width=300, height=400, bg="white")
        self.canvas.pack()

        # Начальные координаты солнца в левом нижнем углу
        self.sun_x = 20
        self.sun_y = 300  # Устанавливаем Y-координату ближе к низу
        self.sun_radius = 30
        self.sun_color = "yellow"
        self.sun_id = self.canvas.create_oval(
            self.sun_x - self.sun_radius,
            self.sun_y - self.sun_radius,
            self.sun_x + self.sun_radius,
            self.sun_y + self.sun_radius,
            fill=self.sun_color,
        )



        self.arrow_x1 = self.sun_x - 10
        self.arrow_y1 = self.sun_y
        self.arrow_x2 = self.sun_x + 10
        self.arrow_y2 = self.sun_y
        self.arrow_id = self.canvas.create_line(
            self.arrow_x1,
            self.arrow_y1,
            self.arrow_x2,
            self.arrow_y2,
            width=2,
            arrow=tk.LAST,
        )
        self.oval_x = 150
        self.oval_y = 800
        self.oval_radius = 500
        self.oval_color = "springgreen1"
        self.oval_id = self.canvas.create_oval(
            self.oval_x - self.oval_radius,
            self.oval_y - self.oval_radius,
            self.oval_x + self.oval_radius,
            self.oval_y + self.oval_radius,
            fill=self.oval_color,
        )
        self.animate_sun()

    def animate_sun(self):
        self.sun_x += 2
        self.sun_y -= 1 #  Двигаем солнце вверх по мере движения вправо
        self.canvas.coords(self.sun_id, self.sun_x - self.sun_radius,
                           self.sun_y - self.sun_radius,
                           self.sun_x + self.sun_radius,
                           self.sun_y + self.sun_radius)
        self.canvas.coords(self.arrow_id, self.sun_x - 5,
                           self.sun_y,
                           self.sun_x + 5,
                           self.sun_y)

        #  Анимация до середины правого края (половина ширины холста)
        if self.sun_x >= 300:
            # Запускаем ScheduleWindow, когда анимация завершится
            self.after(5, lambda: ScheduleWindow(self.user_id).mainloop())
            self.withdraw()
        else:
            self.after(5, self.animate_sun)


class ScheduleWindow(tk.Tk):
    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Расписание")

        self.user_id = user_id

        self.tree = ttk.Treeview(self, columns=("День недели", "первая пара", "вторая пара", "третья пара"), show="headings", height=30)
        self.tree.heading("День недели", text="День недели")
        self.tree.heading("первая пара", text="первая пара")
        self.tree.heading("вторая пара", text="вторая пара")
        self.tree.heading("третья пара", text="третья пара")
        self.tree.pack()

        self.load_schedule()

        self.exit_button = tk.Button(self, text="Выход", command=self.exit, font=("Arial Bold", 25))
        self.exit_button.pack(pady=10)

    def load_schedule(self):
        """Загружает расписание из базы данных."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT day, o_pair, t_pair, th_pair FROM schedule WHERE user_id=?",
            (self.user_id,),
        )
        schedule = cursor.fetchall()
        conn.close()

        for day, o_pair, t_pair, th_pair in schedule:
            self.tree.insert("", tk.END, values=(day, o_pair, t_pair, th_pair))

    def exit(self):
        self.destroy()
        LoginWindow().mainloop()


# Запуск приложения
conn = connect_db()
create_tables(conn)
conn.close()
LoginWindow().mainloop()