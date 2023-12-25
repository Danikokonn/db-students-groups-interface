from .AdminForm import *
from .HumanResForm import *
from .HeadOfDepartForm import *
from .DeanForm import *
from sqlalchemy import create_engine
from tkinter import font


class MainForm(Tk):
    def __init__(
        self,
        engine: str,
        login: str,
        pswd: str,
        host: str,
        port: str,
        database: str,
        dbschema: str,
    ):
        super().__init__()

        self.title("Главное окно")
        self.configure(background="#5FD2B5")

        self.dbengine = create_engine(
            f"{engine}://{login}:{pswd}@{host}:{port}/{database}",
            connect_args={"options": "-csearch_path={}".format(dbschema)},
        )

        font1 = font.Font(family="Arial", size=14)
        font2 = ("calibri", 12, "bold", "underline")

        self.f_head = Frame(self)
        self.f_middle = Frame(self)
        self.f_bot = Frame(self)

        self.f_head.pack(side=TOP, fill=X)
        self.f_middle.pack(side=TOP, expand=1, fill=BOTH)

        self.lbl_head = Label(
            self.f_head,
            text="Интерфейс для работы с базой данных Группы-Студенты\nВыберите пользователя",
            font=font1,
            background="#1F7C65",
            foreground="#9B001C",
        )
        self.lbl_head.pack(side=LEFT, expand=1, fill=X)

        self.btn_goto_admin_form = Button(
            self.f_middle,
            text="Администратор",
            font=font2,
            background="#006C51",
            foreground="#FFB640",
        )
        self.btn_goto_admin_form.bind(
            "<ButtonRelease>", self.on_btn_goto_admin_form_click
        )
        self.btn_goto_admin_form.pack(side=TOP, expand=1, fill=BOTH)

        self.btn_goto_human_res_form = Button(
            self.f_middle,
            text="Сотрудник отдела кадров",
            font=font2,
            background="#006C51",
            foreground="#FFB640",
        )
        self.btn_goto_human_res_form.bind(
            "<ButtonRelease>", self.on_btn_goto_human_res_form_click
        )
        self.btn_goto_human_res_form.pack(side=TOP, expand=1, fill=BOTH)

        self.btn_goto_dean_form = Button(
            self.f_middle,
            text="Сотрудник деканата",
            font=font2,
            background="#006C51",
            foreground="#FFB640",
        )
        self.btn_goto_dean_form.bind(
            "<ButtonRelease>", self.on_btn_goto_dean_form_click
        )
        self.btn_goto_dean_form.pack(side=TOP, expand=1, fill=BOTH)

        self.btn_goto_head_of_depart_form = Button(
            self.f_middle,
            text="Завкафедры",
            font=font2,
            background="#006C51",
            foreground="#FFB640",
        )
        self.btn_goto_head_of_depart_form.bind(
            "<ButtonRelease>", self.on_btn_goto_head_of_depart_form_click
        )
        self.btn_goto_head_of_depart_form.pack(side=TOP, expand=1, fill=BOTH)

    def on_btn_goto_admin_form_click(self, event):
        self.withdraw()
        window = AdminForm(self, self.dbengine)
        window.grab_set()

    def on_btn_goto_human_res_form_click(self, event):
        self.withdraw()
        window = HumanResForm(self, self.dbengine)
        window.grab_set()

    def on_btn_goto_head_of_depart_form_click(self, event):
        self.withdraw()
        window = ChooseDepartForm(self, self.dbengine)
        window.grab_set()

    def on_btn_goto_dean_form_click(self, event):
        self.withdraw()
        window = ChooseDeanForm(self, self.dbengine)
        window.grab_set()
