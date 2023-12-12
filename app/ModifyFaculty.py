from .db_models import *
from tkinter import *
from tkinter.messagebox import showerror, showinfo, showwarning
from sqlalchemy import Engine, exc, select
from sqlalchemy.orm import Session, sessionmaker

class ModifyFaculty(Toplevel):
    def __init__(self, master, engine:Engine):
        super().__init__(master)
        
        self.dbengine = engine

        self.session:Session = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Изменение факультета")

        self.btn_del_fac = Button(self, text="Изменить факультет")
        self.btn_del_fac.bind("<ButtonRelease>", self.on_btn_mod_faculty_clicked,)

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

        self.lbl_infotitle = Label(self, text="Форма для ввода изменений (оставить поле пустым - не изменить)")

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

        self.lblid = Label(self, text="Номер факультета")

        self.str_id = StringVar()

        self.txtid = Entry(self, textvariable=self.str_id)

        self.lblfullname = Label(self, text="Название")

        self.str_fullname = StringVar()

        self.txtfullname = Entry(self, textvariable=self.str_fullname)

        self.lbladdress = Label(self, text="Адрес")

        self.str_address = StringVar()

        self.txtaddress = Entry(self, textvariable=self.str_address)

        self.lbldean_room_num = Label(self, text="Кабинет деканата")

        self.str_dean_room_num = StringVar()

        self.txtdean_room_num = Entry(self, textvariable=self.str_dean_room_num)

        self.lbldean_fullname = Label(self, text="ФИО декана")

        self.str_dean_fullname = StringVar()

        self.txtdean_fullname = Entry(self, textvariable=self.str_dean_fullname)

        self.after_idle(self.on_open)


    def session_manager(func):
        def wrapper(self, event=None, *args, **kwargs):
            if self.session is None or not self.session.is_active:
                self.session = sessionmaker(bind=self.dbengine)()
            try:
                func(self, event, *args, **kwargs)
            except exc.DataError:
                showerror("Ошибка ввода данных!", "Проверьте корректность ввода данных о факультете!")
            except IndexError:
                showerror("Ошибка удаления факультета!", "Отметьте галочкой один факультет, который хотите изменить!")
            except ValueError:
                showwarning("Изменений не произошло!", "Введите изменения в соответсвующие поля!")
            except Exception as e:
                showerror("Неизвестная ошибка!", e, e.args,)
            if self.session.is_active:
                self.session.close()
        return wrapper


    @session_manager
    def on_btn_mod_faculty_clicked(self, event):
        fac = self.session.get(Faculty, self.var.get())
        # Извлечение ввода
        id = self.str_id.get()
        full_name = self.str_fullname.get()
        address = self.str_address.get()
        deans_room_num = self.str_dean_room_num.get()
        dean_full_name = self.str_dean_fullname.get()

        if not any([len(id), len(full_name), len(address), len(deans_room_num), len(dean_full_name)]):
            raise ValueError("all fields are empty")

        if len(id):
            fac.id=id
        if  len(full_name):
            fac.full_name=full_name
        if  len(address):
            fac.address=address
        if  len(deans_room_num):
            fac.deans_room_num=deans_room_num
        if  len(dean_full_name):
            fac.dean_full_name=dean_full_name

        self.session.commit()

        # Очистка ввода
        self.str_id.set('')
        self.str_fullname.set('')
        self.str_address.set('')
        self.str_dean_room_num.set('')
        self.str_dean_fullname.set('')
        for widget in self.winfo_children():
            widget.grid_forget()
        self.on_open()
        showinfo("Операция выполнена успешно!", "Факультет успешно изменён!")
        

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

            self.lbl_id.grid(row=1, column=0)
            self.lbl_fullname.grid(row=1, column=1)
            self.lbl_address.grid(row=1, column=2)
            self.lbl_dean_room_num.grid(row=1, column=3)
            self.lbl_dean_fullname.grid(row=1, column=4)
            
            self.rbuttons[-1].grid(row=idx+2, column=0)
            for i, lbl in enumerate(entry):
                lbl.grid(row=idx+2, column=i+1)

            self.tbl_elems.append(entry)

        last_row = len(facs) + 8
        
        self.lbl_infotitle.grid(row=last_row-3, columnspan=4)

        self.lblid.grid(row=last_row,column=0)
        self.txtid.grid(row=last_row,column=1)
        self.lblfullname.grid(row=last_row+1,column=0)
        self.txtfullname.grid(row=last_row+1,column=1)
        self.lbladdress.grid(row=last_row+2,column=0)
        self.txtaddress.grid(row=last_row+2,column=1)
        self.lbldean_room_num.grid(row=last_row+3,column=0)
        self.txtdean_room_num.grid(row=last_row+3,column=1)
        self.lbldean_fullname.grid(row=last_row+4,column=0)
        self.txtdean_fullname.grid(row=last_row+4,column=1)

        self.btn_del_fac.grid(row=last_row+5, column=0)
        self.btn_back.grid(row=last_row+5, column=1)

