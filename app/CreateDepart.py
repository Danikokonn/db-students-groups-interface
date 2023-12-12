from .db_models import *
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from sqlalchemy import Engine, exc
from sqlalchemy.orm import Session, sessionmaker
from psycopg2.errors import ForeignKeyViolation, UniqueViolation

class CreateDepart(Toplevel):
    def __init__(self, master, engine:Engine):
        super().__init__(master)
        
        self.dbengine = engine

        self.session:Session = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Формирование кафедры")

        self.btn_create_depart = Button(self, text="Создать кафедру")
        self.btn_create_depart.bind("<ButtonRelease>", self.on_btn_add_depart_clicked,)
        self.btn_create_depart.grid(row=6,column=0)

        self.btn_back = Button(self, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked,)
        self.btn_back.grid(row=6,column=1)

        self.lbl_id = Label(self, text="Номер кафедры")
        self.lbl_id.grid(row=0,column=0)

        self.str_id = StringVar()

        self.txt_id = Entry(self, textvariable=self.str_id)
        self.txt_id.grid(row=0,column=1)

        self.lbl_fullname = Label(self, text="Название")
        self.lbl_fullname.grid(row=1,column=0)

        self.str_fullname = StringVar()

        self.txt_fullname = Entry(self, textvariable=self.str_fullname)
        self.txt_fullname.grid(row=1,column=1)

        self.lbl_address = Label(self, text="Адрес")
        self.lbl_address.grid(row=2,column=0)

        self.str_address = StringVar()

        self.txt_address = Entry(self, textvariable=self.str_address)
        self.txt_address.grid(row=2,column=1)

        self.lbl_depart_room_num = Label(self, text="Кабинет кафедры")
        self.lbl_depart_room_num.grid(row=3,column=0)

        self.str_depart_room_num = StringVar()

        self.txt_depart_room_num = Entry(self, textvariable=self.str_depart_room_num)
        self.txt_depart_room_num.grid(row=3,column=1)

        self.lbl_head_of_depart_fullname = Label(self, text="ФИО завкафедры")
        self.lbl_head_of_depart_fullname.grid(row=4,column=0)

        self.str_head_of_depart_fullname = StringVar()

        self.txt_head_of_depart_fullname = Entry(self, textvariable=self.str_head_of_depart_fullname)
        self.txt_head_of_depart_fullname.grid(row=4,column=1)

        self.lbl_faculty_id = Label(self, text="Номер факультета")
        self.lbl_faculty_id.grid(row=5,column=0)

        self.str_faculty_id = StringVar()

        self.txt_faculty_id = Entry(self, textvariable=self.str_faculty_id)
        self.txt_faculty_id.grid(row=5,column=1)
        

    def session_manager(func):
        def wrapper(self, event, *args, **kwargs):
            if self.session is None or not self.session.is_active:
                self.session = sessionmaker(bind=self.dbengine)()
            try:
                func(self, event, *args, **kwargs)
                showinfo("Операция выполнена успешно!", "Кафедра успешно создана!")
            except exc.DataError:
                showerror("Ошибка ввода данных!", "Проверьте корректность ввода данных о кафедре!")
            except exc.IntegrityError as e:
                if "violates foreign key" in e.orig:
                    showerror("Ошибка добавления Кафедры!", "Попытка привязать кафедру к несуществующему факультету!")
                elif "violates unique constraint" in e.orig:
                    showerror("Ошибка добавления Кафедры!", "Кафедра с данным номером уже существует!")
            except Exception as e:
                showerror("Неизвестная ошибка!", e.args)
            if self.session.is_active:
                self.session.close()
        return wrapper


    @session_manager
    def on_btn_add_depart_clicked(self, event):
        # Извлечение ввода
        id = self.str_id.get()
        full_name = self.str_fullname.get()
        address = self.str_address.get()
        depart_room_num = self.str_depart_room_num.get()
        head_of_depart_fullname = self.str_head_of_depart_fullname.get()
        faculty_id = self.str_faculty_id.get()

        # Вставка записи
        depart_to_add = Department(
            id=id, 
            full_name=full_name, 
            address=address, 
            depart_room_num=depart_room_num, 
            head_of_depart_full_name=head_of_depart_fullname,
            faculty_id=faculty_id
        )
        self.session.add(depart_to_add)
        self.session.commit()

        # Очистка ввода
        self.str_id.set('')
        self.str_fullname.set('')
        self.str_address.set('')
        self.str_depart_room_num.set('')
        self.str_head_of_depart_fullname.set('')
        self.str_faculty_id.set('')
        
    def on_btn_back_clicked(self, event):
        self.on_closing(event)

    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()

