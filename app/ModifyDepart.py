from .db_models import *
from tkinter import *
from tkinter.messagebox import showerror, showinfo, showwarning
from sqlalchemy import Engine, exc, select
from sqlalchemy.orm import Session, sessionmaker

class ModifyDepart(Toplevel):
    def __init__(self, master, engine:Engine):
        super().__init__(master)
        
        self.dbengine = engine

        self.session:Session = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Изменение кафедры")

        self.btn_mod_depart = Button(self, text="Изменить кафедру")
        self.btn_mod_depart.bind("<ButtonRelease>", self.on_btn_mod_depart_clicked,)

        self.btn_back = Button(self, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked,)
    
        self.str_id = StringVar()
        self.str_fullname = StringVar()
        self.str_address = StringVar()
        self.str_depart_room_num = StringVar()
        self.str_head_of_depart_fullname = StringVar()
        self.str_faculty_id = StringVar()

        self.var = StringVar()

        self.rbuttons = []
        self.tbl_elems = []

        self.lbl_infotitle = Label(self, text="Форма для ввода изменений (оставить поле пустым - не изменять)")

        self.lbl_id = Label(self, text="Номер кафедры")
        self.lbl_id.grid(row=1, column=0)

        self.lbl_fullname = Label(self, text="Название")
        self.lbl_fullname.grid(row=1, column=1)

        self.lbl_address = Label(self, text="Адрес")
        self.lbl_address.grid(row=1, column=2)

        self.lbl_depart_room_num = Label(self, text="Кабинет кафедры")
        self.lbl_depart_room_num.grid(row=1, column=3)

        self.lbl_head_of_depart_fullname = Label(self, text="ФИО завкафедры")
        self.lbl_head_of_depart_fullname.grid(row=1, column=4)

        self.lbl_faculty_id = Label(self, text="Номер факультета")
        self.lbl_faculty_id.grid(row=1, column=5)

        self.lbl_id2 = Label(self, text="Номер кафедры")
        self.lbl_id2.grid(row=0,column=0)

        self.str_id2 = StringVar()

        self.txt_id2 = Entry(self, textvariable=self.str_id)
        self.txt_id2.grid(row=0,column=1)

        self.lbl_fullname2 = Label(self, text="Название")
        self.lbl_fullname2.grid(row=1,column=0)

        self.str_fullname2 = StringVar()

        self.txt_fullname2 = Entry(self, textvariable=self.str_fullname)
        self.txt_fullname2.grid(row=1,column=1)

        self.lbl_address2 = Label(self, text="Адрес")
        self.lbl_address2.grid(row=2,column=0)

        self.str_address2 = StringVar()

        self.txt_address2 = Entry(self, textvariable=self.str_address)
        self.txt_address2.grid(row=2,column=1)

        self.lbl_depart_room_num2 = Label(self, text="Кабинет кафедры")
        self.lbl_depart_room_num2.grid(row=3,column=0)

        self.str_depart_room_num2 = StringVar()

        self.txt_depart_room_num2 = Entry(self, textvariable=self.str_depart_room_num)
        self.txt_depart_room_num2.grid(row=3,column=1)

        self.lbl_head_of_depart_fullname2 = Label(self, text="ФИО завкафедры")
        self.lbl_head_of_depart_fullname2.grid(row=4,column=0)

        self.str_head_of_depart_fullname2 = StringVar()

        self.txt_head_of_depart_fullname2 = Entry(self, textvariable=self.str_head_of_depart_fullname)
        self.txt_head_of_depart_fullname2.grid(row=4,column=1)

        self.lbl_faculty_id2 = Label(self, text="Номер факультета")
        self.lbl_faculty_id2.grid(row=5,column=0)

        self.str_faculty_id2 = StringVar()

        self.txt_faculty_id2 = Entry(self, textvariable=self.str_faculty_id)
        self.txt_faculty_id2.grid(row=5,column=1)

        self.after_idle(self.on_open)


    def session_manager(func):
        def wrapper(self, event=None, *args, **kwargs):
            if self.session is None or not self.session.is_active:
                self.session = sessionmaker(bind=self.dbengine)()
            try:
                func(self, event, *args, **kwargs)
            except exc.DataError:
                showerror("Ошибка ввода данных!", "Проверьте корректность ввода данных о кафедре!")
            except IndexError:
                showerror("Ошибка удаления факультета!", "Отметьте галочкой одну кафедру, которую хотите изменить!")
            except ValueError:
                showwarning("Изменений не произошло!", "Введите изменения в соответсвующие поля!")
            except Exception as e:
                showerror("Неизвестная ошибка!", e, e.args,)
            if self.session.is_active:
                self.session.close()
        return wrapper


    @session_manager
    def on_btn_mod_depart_clicked(self, event):
        depart = self.session.get(Department, self.var.get())
        # Извлечение ввода
        id = self.str_id.get()
        full_name = self.str_fullname.get()
        address = self.str_address.get()
        depart_room_num = self.str_depart_room_num.get()
        head_of_depart_fullname = self.str_head_of_depart_fullname.get()
        faculty_id = self.str_faculty_id.get()

        if not any([len(id), len(full_name), len(address), len(depart_room_num), len(head_of_depart_fullname), len(faculty_id)]):
            raise ValueError("all fields are empty")

        if len(id):
            depart.id=id
        if  len(full_name):
            depart.full_name=full_name
        if  len(address):
            depart.address=address
        if  len(depart_room_num):
            depart.depart_room_num=depart_room_num
        if  len(head_of_depart_fullname):
            depart.head_of_depart_full_name=head_of_depart_fullname
        if  len(faculty_id):
            depart.faculty_id=faculty_id

        self.session.commit()

        # Очистка ввода
        self.str_id.set('')
        self.str_fullname.set('')
        self.str_address.set('')
        self.str_depart_room_num.set('')
        self.str_head_of_depart_fullname.set('')
        self.str_faculty_id.set('')
        for widget in self.winfo_children():
            widget.grid_forget()
        self.on_open()
        showinfo("Операция выполнена успешно!", "Кафедра успешно изменена!")
        

    def on_btn_back_clicked(self, event):
        self.on_closing(event)


    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()

    
    @session_manager
    def on_open(self, event=None):
        stmt = select(Department).order_by(Department.id)
        departs = self.session.scalars(stmt).all()
        self.tbl_elems.clear()
        self.rbuttons.clear()

        self.lbl_id.grid(row=1, column=0)
        self.lbl_fullname.grid(row=1, column=1)
        self.lbl_address.grid(row=1, column=2)
        self.lbl_depart_room_num.grid(row=1, column=3)
        self.lbl_head_of_depart_fullname.grid(row=1, column=4)
        self.lbl_faculty_id.grid(row=1, column=5)

        self.var.set(departs[0].id)
        for idx, depart in enumerate(departs):
            text, value = (depart.id, depart.id)
            self.rbuttons.append(Radiobutton(self,text=text, value=value, variable=self.var))
            entry = [
                Label(self, text=depart.full_name), 
                Label(self, text=depart.address),
                Label(self, text=depart.depart_room_num), 
                Label(self, text=depart.head_of_depart_full_name),
                Label(self, text=depart.faculty_id)
            ]
            
            self.rbuttons[-1].grid(row=idx+2, column=0)
            for i, lbl in enumerate(entry):
                lbl.grid(row=idx+2, column=i+1)

            self.tbl_elems.append(entry)

        last_row = len(departs) + 8
        
        self.lbl_infotitle.grid(row=last_row-3, columnspan=4)

        self.lbl_id2.grid(row=last_row,column=0)
        self.txt_id2.grid(row=last_row,column=1)
        self.lbl_fullname2.grid(row=last_row+1,column=0)
        self.txt_fullname2.grid(row=last_row+1,column=1)
        self.lbl_address2.grid(row=last_row+2,column=0)
        self.txt_address2.grid(row=last_row+2,column=1)
        self.lbl_depart_room_num2.grid(row=last_row+3,column=0)
        self.txt_depart_room_num2.grid(row=last_row+3,column=1)
        self.lbl_head_of_depart_fullname2.grid(row=last_row+4,column=0)
        self.txt_head_of_depart_fullname2.grid(row=last_row+4,column=1)
        self.lbl_faculty_id2.grid(row=last_row+5,column=0)
        self.txt_faculty_id2.grid(row=last_row+5,column=1)

        self.btn_mod_depart.grid(row=last_row+6, column=0)
        self.btn_back.grid(row=last_row+6, column=1)

