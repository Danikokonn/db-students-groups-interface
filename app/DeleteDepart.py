from .db_models import *
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from sqlalchemy import Engine, exc, select
from sqlalchemy.orm import Session, sessionmaker

class DeleteDepart(Toplevel):
    def __init__(self, master, engine:Engine):
        super().__init__(master)
        
        self.dbengine = engine

        self.session:Session = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Удаление кафедры")

        self.btn_del_depart = Button(self, text="Удалить кафедру")
        self.btn_del_depart.bind("<ButtonRelease>", self.on_btn_del_depart_clicked,)

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

        self.after_idle(self.on_open)


    def session_manager(func):
        def wrapper(self, event=None, *args, **kwargs):
            if self.session is None or not self.session.is_active:
                self.session = sessionmaker(bind=self.dbengine)()
            try:
                func(self, event, *args, **kwargs)
            except IndexError:
                showerror("Ошибка удаления кафедры!", "Отметьте галочкой одну кафедру, которую хотите удалить!")
            except Exception as e:
                showerror("Неизвестная ошибка!", e.args)
            if self.session.is_active:
                self.session.close()
        return wrapper


    @session_manager
    def on_btn_del_depart_clicked(self, event):
        # Извлечение ввода
        depart = self.session.get(Department, self.var.get())
        self.session.delete(depart)
        self.session.commit()
        for widget in self.winfo_children():
            widget.grid_forget()
        self.on_open()
        showinfo("Операция выполнена успешно!", "Кафедра успешно удалена!")
        

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

            self.btn_del_depart.grid(row=0, column=0)
            self.btn_back.grid(row=0, column=1)

            self.lbl_id.grid(row=1, column=0)
            self.lbl_fullname.grid(row=1, column=1)
            self.lbl_address.grid(row=1, column=2)
            self.lbl_depart_room_num.grid(row=1, column=3)
            self.lbl_head_of_depart_fullname.grid(row=1, column=4)
            self.lbl_faculty_id.grid(row=1, column=5)
            
            self.rbuttons[-1].grid(row=idx+2, column=0)
            for i, lbl in enumerate(entry):
                lbl.grid(row=idx+2, column=i+1)

            self.tbl_elems.append(entry)

