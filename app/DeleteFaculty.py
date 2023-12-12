from .db_models import *
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from sqlalchemy import Engine, exc, select
from sqlalchemy.orm import Session, sessionmaker

class DeleteFaculty(Toplevel):
    def __init__(self, master, engine:Engine):
        super().__init__(master)
        
        self.dbengine = engine

        self.session:Session = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Удаление факультета")

        self.btn_del_fac = Button(self, text="Удалить факультет")
        self.btn_del_fac.bind("<ButtonRelease>", self.on_btn_del_faculty_clicked,)

        self.btn_back = Button(self, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked,)
    
        self.str_id = StringVar()
        self.str_fullname = StringVar()
        self.str_address = StringVar()
        self.str_dean_room_num = StringVar()
        self.str_dean_fullname = StringVar()

        self.var = StringVar()

        self.rbuttons = []
        self.tbl_elems = []

        self.lbl_id = Label(self, text="Номер факультета")
        self.lbl_id.grid(row=1, column=0)

        self.lbl_fullname = Label(self, text="Название")
        self.lbl_fullname.grid(row=1, column=1)

        self.lbl_address = Label(self, text="Адрес")
        self.lbl_address.grid(row=1, column=2)

        self.lbl_dean_room_num = Label(self, text="Кабинет деканата")
        self.lbl_dean_room_num.grid(row=1, column=3)

        self.lbl_dean_fullname = Label(self, text="ФИО декана")
        self.lbl_dean_fullname.grid(row=1, column=4)

        self.after_idle(self.on_open)


    def session_manager(func):
        def wrapper(self, event=None, *args, **kwargs):
            if self.session is None or not self.session.is_active:
                self.session = sessionmaker(bind=self.dbengine)()
            try:
                func(self, event, *args, **kwargs)
            except IndexError:
                showerror("Ошибка удаления факультета!", "Отметьте галочкой один факультет, который хотите удалить!")
            except Exception as e:
                showerror("Неизвестная ошибка!", e.args)
            if self.session.is_active:
                self.session.close()
        return wrapper


    @session_manager
    def on_btn_del_faculty_clicked(self, event):
        # Извлечение ввода
        fac = self.session.get(Faculty, self.var.get())
        self.session.delete(fac)
        self.session.commit()
        for widget in self.winfo_children():
            widget.grid_forget()
        self.on_open()
        showinfo("Операция выполнена успешно!", "Факультет успешно удалён!")
        

    def on_btn_back_clicked(self, event):
        self.on_closing(event)


    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()

    
    @session_manager
    def on_open(self, event=None):
        stmt = select(Faculty).order_by(Faculty.id)
        facs = self.session.scalars(stmt).all()
        self.tbl_elems.clear()
        self.rbuttons.clear()

        self.var.set(facs[0].id)
        for idx, fac in enumerate(facs):
            text, value = (fac.id, fac.id)
            self.rbuttons.append(Radiobutton(self,text=text, value=value, variable=self.var))
            entry = [
                Label(self, text=fac.full_name), 
                Label(self, text=fac.address),
                Label(self, text=fac.deans_room_num), 
                Label(self, text=fac.dean_full_name)
            ]

            self.btn_del_fac.grid(row=0, column=0)
            self.btn_back.grid(row=0, column=1)

            self.lbl_id.grid(row=1, column=0)
            self.lbl_fullname.grid(row=1, column=1)
            self.lbl_address.grid(row=1, column=2)
            self.lbl_dean_room_num.grid(row=1, column=3)
            self.lbl_dean_fullname.grid(row=1, column=4)
            
            self.rbuttons[-1].grid(row=idx+2, column=0)
            for i, lbl in enumerate(entry):
                lbl.grid(row=idx+2, column=i+1)

            self.tbl_elems.append(entry)

