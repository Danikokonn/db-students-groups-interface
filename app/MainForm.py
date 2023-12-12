from .AdminForm import *
from sqlalchemy import create_engine
from tkinter import font


class MainForm(Tk):
    def __init__(self, engine:str, login:str, pswd:str, host:str, port:str, database:str, dbschema:str):
        super().__init__()
        
        self.title("Главное окно")

        self.dbengine = create_engine(f'{engine}://{login}:{pswd}@{host}:{port}/{database}', connect_args={'options': '-csearch_path={}'.format(dbschema)})

        font1 = font.Font(family="Arial", size=14)

        self.btn_goto_admin_form = Button(self, text="Администратор", font=font1)
        self.btn_goto_admin_form.bind("<ButtonRelease>", self.on_btn_goto_admin_form_click)
        self.btn_goto_admin_form.grid(row=2, column=0, rowspan=2, columnspan=4, sticky="W")

        self.btn_goto_ok_form = Button(self, text="Сотрудник отдела кадров", font=font1)
        self.btn_goto_ok_form.bind("<ButtonRelease>", self.on_btn_goto_ok_form_click)
        self.btn_goto_ok_form.grid(row=4, column=0, rowspan=2, columnspan=4, sticky="W")

        self.btn_goto_dean_form = Button(self, text="Сотрудник деканата", font=font1)
        self.btn_goto_dean_form.bind("<ButtonRelease>", self.on_btn_goto_dean_form_click)
        self.btn_goto_dean_form.grid(row=6, column=0, rowspan=2, columnspan=4, sticky="W")

        self.btn_goto_head_of_depart_form = Button(self, text="Завкафедры", font=font1)
        self.btn_goto_head_of_depart_form.bind("<ButtonRelease>", self.on_btn_goto_head_of_depart_form_click)
        self.btn_goto_head_of_depart_form.grid(row=8, column=0, rowspan=2, columnspan=4, sticky="W")

        self.txtbx1 = Label(self, width=22, height=1, text="Выберите пользователя", font=font1)
        self.txtbx1.grid(row=0, column=0, rowspan=2, columnspan=4, sticky="W")



    def on_btn_goto_admin_form_click(self, event):
        self.withdraw()
        window = AdminForm(self, self.dbengine)
        window.grab_set()


    def on_btn_goto_ok_form_click(self, event):
        pass


    def on_btn_goto_dean_form_click(self, event):
        pass


    def on_btn_goto_head_of_depart_form_click(self, event):
        pass

