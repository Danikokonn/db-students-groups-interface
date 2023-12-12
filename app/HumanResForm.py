from .db_models import *
from .TreeViewRead import *
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from sqlalchemy import Engine, exc
from sqlalchemy.orm import Session, sessionmaker



class HumanResForm(Toplevel):
    def __init__(self, master, engine:Engine):
        super().__init__(master)

        self.dbengine=engine

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Окно сотрудника отдела кадров")

        # Кнопка treeview
        self.btn_goto_treeview = Button(self, text="Просмотр данных")
        self.btn_goto_treeview.bind("<ButtonRelease>", self.on_btn_goto_treeview_click)
        self.btn_goto_treeview.grid(row=0, column=0)

        # Общие кнопки
        self.btn_back = Button(self, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked)
        self.btn_back.grid(row=1, column=0)


    # Обработчик treeview
    def on_btn_goto_treeview_click(self, event):
        self.withdraw()
        window = TreeViewRead(self, self.dbengine)
        window.grab_set()


    # Общие обработчики
    def on_btn_back_clicked(self, event):
        self.on_closing(event)


    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()

