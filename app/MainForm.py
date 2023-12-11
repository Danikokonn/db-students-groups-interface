from .AdminForm import *
from sqlalchemy import create_engine


class MainForm(Tk):
    def __init__(self, engine:str, login:str, pswd:str, host:str, port:str, database:str, dbschema:str):
        super().__init__()
        
        self.geometry("300x200")
        self.title("Главное окно")

        self.dbengine = create_engine(f'{engine}://{login}:{pswd}@{host}:{port}/{database}', connect_args={'options': '-csearch_path={}'.format(dbschema)})

        self.btn_goto_admin_form = Button(self, text="Администратор")
        self.btn_goto_admin_form.bind("<ButtonRelease>", self.on_btn_goto_admin_form_click)
        self.btn_goto_admin_form.place(x=50, y=50)

        self.btn_goto_ok_form = Button(self, text="Сотрудник отдела кадров")
        self.btn_goto_ok_form.bind("<ButtonRelease>", self.on_btn_goto_ok_form_click)
        self.btn_goto_ok_form.place(x=50, y=100)

        self.btn_goto_dean_form = Button(self, text="Сотрудник деканата")
        self.btn_goto_dean_form.bind("<ButtonRelease>", self.on_btn_goto_dean_form_click)
        self.btn_goto_dean_form.place(x=50, y=150)

        self.btn_goto_head_of_depart_form = Button(self, text="Завкафедры")
        self.btn_goto_head_of_depart_form.bind("<ButtonRelease>", self.on_btn_goto_head_of_depart_form_click)
        self.btn_goto_head_of_depart_form.place(x=50, y=200)

        self.txtbx1 = Label(self, width=22, height=1, text="Выберите пользователя")
        self.txtbx1.place(y=10, x=50)



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

