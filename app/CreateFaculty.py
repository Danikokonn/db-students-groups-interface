from .db_models import *
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from sqlalchemy import Engine, exc
from sqlalchemy.orm import Session, sessionmaker

class CreateFaculty(Toplevel):
    def __init__(self, master, engine:Engine):
        super().__init__(master)
        
        self.dbengine = engine

        self.session:Session = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Формирование факультета")

        self.btn_create_fac = Button(self, text="Создать факультет")
        self.btn_create_fac.bind("<ButtonRelease>", self.on_btn_add_faculty_clicked,)
        self.btn_create_fac.grid(row=5,column=0)

        self.btn_back = Button(self, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked,)
        self.btn_back.grid(row=5,column=1)

        self.lblid = Label(self, text="Номер факультета")
        self.lblid.grid(row=0,column=0)

        self.str_id = StringVar()

        self.txtid = Entry(self, textvariable=self.str_id)
        self.txtid.grid(row=0,column=1)

        self.lblfullname = Label(self, text="Название")
        self.lblfullname.grid(row=1,column=0)

        self.str_fullname = StringVar()

        self.txtfullname = Entry(self, textvariable=self.str_fullname)
        self.txtfullname.grid(row=1,column=1)

        self.lbladdress = Label(self, text="Адрес")
        self.lbladdress.grid(row=2,column=0)

        self.str_address = StringVar()

        self.txtaddress = Entry(self, textvariable=self.str_address)
        self.txtaddress.grid(row=2,column=1)

        self.lbldean_room_num = Label(self, text="Кабинет деканата")
        self.lbldean_room_num.grid(row=3,column=0)

        self.str_dean_room_num = StringVar()

        self.txtdean_room_num = Entry(self, textvariable=self.str_dean_room_num)
        self.txtdean_room_num.grid(row=3,column=1)

        self.lbldean_fullname = Label(self, text="ФИО декана")
        self.lbldean_fullname.grid(row=4,column=0)

        self.str_dean_fullname = StringVar()

        self.txtdean_fullname = Entry(self, textvariable=self.str_dean_fullname)
        self.txtdean_fullname.grid(row=4,column=1)


    def session_manager(func):
        def wrapper(self, event, *args, **kwargs):
            if self.session is None or not self.session.is_active:
                self.session = sessionmaker(bind=self.dbengine)()
            try:
                func(self, event, *args, **kwargs)
                showinfo("Операция выполнена успешно!", "Факультет успешно создан!")
            except exc.DataError:
                showerror("Ошибка ввода данных!", "Проверьте корректность ввода данных о факультете!")
            except exc.IntegrityError:
                showerror("Ошибка добавления факультета!", "Факультет с данным номером уже существует!")
            except Exception as e:
                showerror("Неизвестная ошибка!", e.args)
            if self.session.is_active:
                self.session.close()
        return wrapper


    @session_manager
    def on_btn_add_faculty_clicked(self, event):
        # Извлечение ввода
        id = self.str_id.get()
        full_name = self.str_fullname.get()
        address = self.str_address.get()
        deans_room_num = self.str_dean_room_num.get()
        dean_full_name = self.str_dean_fullname.get()

        # Вставка записи
        faculty_to_add = Faculty(
            id=id, 
            full_name=full_name, 
            address=address, 
            deans_room_num=deans_room_num, 
            dean_full_name=dean_full_name
        )
        self.session.add(faculty_to_add)
        self.session.commit()

        # Очистка ввода
        self.str_id.set('')
        self.str_fullname.set('')
        self.str_address.set('')
        self.str_dean_room_num.set('')
        self.str_dean_fullname.set('')
        
    def on_btn_back_clicked(self, event):
        self.on_closing(event)

    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()

