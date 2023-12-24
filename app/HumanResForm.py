from .db_models import *
from .TreeViewRead import *
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from sqlalchemy import Engine, exc
from sqlalchemy.orm import Session, sessionmaker


class HumanResForm(Toplevel):
    def __init__(self, master, engine: Engine):
        super().__init__(master)

        self.dbengine = engine

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Окно сотрудника отдела кадров")

        self.h_frame = Frame(self)
        self.f_top = Frame(self)
        self.f_bot = Frame(self)

        self.h_frame.pack(side=TOP, fill=X, pady=10)
        self.f_top.pack(side=TOP, expand=1, fill=BOTH, pady=10)
        self.f_bot.pack(side=TOP, fill=X, pady=10)

        self.lbl_head = Label(
            self.h_frame, text="Окно сотрудника отдела кадров\nВыберите действие"
        )
        self.lbl_head.pack(side=TOP, expand=1, fill=X, padx=10)

        # Кнопка treeview
        self.btn_goto_treeview = Button(self.f_top, text="Просмотр данных о студентах")
        self.btn_goto_treeview.bind("<ButtonRelease>", self.on_btn_goto_treeview_click)
        self.btn_goto_treeview.pack(side=TOP, expand=1, fill=BOTH, padx=10)

        # Общие кнопки
        self.btn_back = Button(self.f_bot, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked)
        self.btn_back.pack(side=LEFT, fill=X, padx=10)

    # Обработчик treeview
    def on_btn_goto_treeview_click(self, event):
        self.withdraw()
        window = TreeViewRead(self, self.dbengine, Faculty)
        window.grab_set()

    # Общие обработчики
    def on_btn_back_clicked(self, event):
        self.on_closing(event)

    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()
