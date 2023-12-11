from .db_models import *
from tkinter import *
from tkinter.messagebox import showerror
from sqlalchemy import Engine, exc
from sqlalchemy.orm import Session, sessionmaker

class CreateFaculty(Toplevel):
    def __init__(self, master, engine:Engine):
        super().__init__(master)
        
        self.dbengine = engine

        self.session:Session = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.geometry("300x200")
        self.title("Формирование факультета")

        self.btn1 = Button(self, text="Создать факультет")
        self.btn1.bind("<ButtonRelease>", self.on_btn_add_faculty_clicked,)
        self.btn1.place(x=20, y=120)

        self.lblid = Label(self, text="Номер факультета")
        self.lblid.place(y=10, x=20)

        self.txtid = Entry(self)
        self.txtid.place(y=10, x=150)

        self.lblfullname = Label(self, text="Название")
        self.lblfullname.place(y=30, x=20)

        self.txtfullname = Entry(self)
        self.txtfullname.place(y=30, x=150)

        self.lbladdress = Label(self, text="Адрес")
        self.lbladdress.place(y=50, x=20)

        self.txtaddress = Entry(self)
        self.txtaddress.place(y=50, x=150)

        self.lbldean_room_num = Label(self, text="Кабинет деканата")
        self.lbldean_room_num.place(y=70, x=20)

        self.txtdean_room_num = Entry(self)
        self.txtdean_room_num.place(y=70, x=150)

        self.lbldean_room_num = Label(self, text="ФИО декана")
        self.lbldean_room_num.place(y=90, x=20)

        self.txtdean_fullname = Entry(self)
        self.txtdean_fullname.place(y=90, x=150)

    def session_manager(func):
        def wrapper(self, event, *args, **kwargs):
            self.session = sessionmaker(bind=self.dbengine)()
            try:
                func(self, event, *args, **kwargs)
            except exc.DataError:
                showerror("Ошибка ввода данных!", "Проверьте корректность ввода данных о факультете!")
            except exc.IntegrityError:
                showerror("Ошибка добавления факультета!", "Факультет с данным номером уже существует!")
            except Exception as e:
                showerror("Неизвестная ошибка!", e.args)
            self.session.close()
        return wrapper

    @session_manager
    def on_btn_add_faculty_clicked(self, event):
        id = self.txtid.get()
        full_name = self.txtfullname.get()
        address = self.txtaddress.get()
        deans_room_num = self.txtdean_room_num.get()
        dean_full_name = self.txtdean_fullname.get()

        faculty_to_add = Faculty(
            id=id, 
            full_name=full_name, 
            address=address, 
            deans_room_num=deans_room_num, 
            dean_full_name=dean_full_name
        )
        self.session.add(faculty_to_add)
        self.session.commit()

        print(event.x, event.y)
    
    def on_closing(self):
        self.master.deiconify()
        self.destroy()

