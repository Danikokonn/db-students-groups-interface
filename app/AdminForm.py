from .CreateFaculty import *
from .ModifyFaculty import *
from .DeleteFaculty import *
from .CreateDepart import *
from .ModifyDepart import *
from .DeleteDepart import *

class AdminForm(Toplevel):
    def __init__(self, master, engine:Engine):
        super().__init__(master)

        self.dbengine=engine

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Окно администратора")

        # Кнопки faculty
        self.btn_goto_crt_faculty = Button(self, text="Создание факультета")
        self.btn_goto_crt_faculty.bind("<ButtonRelease>", self.on_btn_goto_create_faculty_click)
        self.btn_goto_crt_faculty.grid(row=0, column=0)

        self.btn_goto_mod_faculty = Button(self, text="Изменение факультета")
        self.btn_goto_mod_faculty.bind("<ButtonRelease>", self.on_btn_goto_mod_faculty_click)
        self.btn_goto_mod_faculty.grid(row=1, column=0)

        self.btn_goto_del_faculty = Button(self, text="Удаление факультета")
        self.btn_goto_del_faculty.bind("<ButtonRelease>", self.on_btn_goto_del_faculty_click)
        self.btn_goto_del_faculty.grid(row=2, column=0)

        # Кнопки depart
        self.btn_goto_crt_depart = Button(self, text="Создание кафедры")
        self.btn_goto_crt_depart.bind("<ButtonRelease>", self.on_btn_goto_create_depart_click)
        self.btn_goto_crt_depart.grid(row=0, column=1)

        self.btn_goto_mod_depart = Button(self, text="Изменение кафедры")
        self.btn_goto_mod_depart.bind("<ButtonRelease>", self.on_btn_goto_mod_depart_click)
        self.btn_goto_mod_depart.grid(row=1, column=1)

        self.btn_goto_del_depart = Button(self, text="Удаление кафедры")
        self.btn_goto_del_depart.bind("<ButtonRelease>", self.on_btn_goto_del_depart_click)
        self.btn_goto_del_depart.grid(row=2, column=1)

        # Общие кнопки
        self.btn_back = Button(self, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked)
        self.btn_back.grid(row=3, column=0)


    # Обработчики faculty
    def on_btn_goto_create_faculty_click(self, event):
        self.withdraw()
        window = CreateFaculty(self, self.dbengine)
        window.grab_set()


    def on_btn_goto_mod_faculty_click(self, event):
        self.withdraw()
        window = ModifyFaculty(self, self.dbengine)
        window.grab_set()


    def on_btn_goto_del_faculty_click(self, event):
        self.withdraw()
        window = DeleteFaculty(self, self.dbengine)
        window.grab_set()


    # Обработчики depart
    def on_btn_goto_create_depart_click(self, event):
        self.withdraw()
        window = CreateDepart(self, self.dbengine)
        window.grab_set()


    def on_btn_goto_mod_depart_click(self, event):
        self.withdraw()
        window = ModifyDepart(self, self.dbengine)
        window.grab_set()


    def on_btn_goto_del_depart_click(self, event):
        self.withdraw()
        window = DeleteDepart(self, self.dbengine)
        window.grab_set()


    # Общие обработчики
    def on_btn_back_clicked(self, event):
        self.on_closing(event)


    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()

