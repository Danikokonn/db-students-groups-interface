from .db_models import *
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from sqlalchemy import Engine, exc, select
from sqlalchemy.orm import Session, sessionmaker

class DeleteForm(Toplevel):
    def __init__(self, master, engine:Engine, cls):
        super().__init__(master)
        
        self.dbengine = engine

        self.session:Session = None

        self.current_class = cls

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title(f"Удаление объекта {self.current_class.desc}")

        self.btn_del = Button(self, text=f"Удалить объект {self.current_class.desc}")
        self.btn_del.bind("<ButtonRelease>", self.on_btn_del_clicked,)

        self.btn_back = Button(self, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked,)

        self.var_deleted = StringVar()

        self.rbuttons = []
        self.tbl_elems = []

        self.lbls_head:dict[str, Label] = {} # Метки шапки таблицы

        for idx, k in enumerate(self.current_class.field_names.keys()):
            self.lbls_head[k] = Label(self, text=self.current_class.field_names[k])
            self.lbls_head[k].grid(row=1, column=idx)

        self.after_idle(self.on_open)


    def session_manager(func):
        def wrapper(self, event=None, *args, **kwargs):
            if self.session is None or not self.session.is_active:
                self.session = sessionmaker(bind=self.dbengine)()
            try:
                func(self, event, *args, **kwargs)
            except IndexError:
                showerror("Ошибка!", "Объектов нет!")
                self.on_closing(event)
            except Exception as e:
                showerror("Неизвестная ошибка!", e.args)
            if self.session.is_active:
                self.session.close()
        return wrapper


    @session_manager
    def on_btn_del_clicked(self, event):
        obj = self.session.get(self.current_class, self.var_deleted.get())
        self.session.delete(obj)
        self.session.commit()
        for widget in self.winfo_children():
            widget.grid_forget()
        self.on_open()
        showinfo("Операция выполнена успешно!", "Объект успешно удалён!")
        

    def on_btn_back_clicked(self, event):
        self.on_closing(event)


    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()

    
    @session_manager
    def on_open(self, event=None):
        stmt = select(self.current_class).order_by(self.current_class.id)
        objs = self.session.scalars(stmt).all()
        self.tbl_elems.clear()
        self.rbuttons.clear()

        for idx, k in enumerate(self.current_class.field_names.keys()):
            self.lbls_head[k].grid(row=0, column=idx)

        self.var_deleted.set(objs[0].id)
        for idx, obj in enumerate(objs):
            text, value = (obj.id, obj.id)
            self.rbuttons.append(Radiobutton(self, text=text, value=value, variable=self.var_deleted))
            entry = [ Label(self, text=getattr(obj, attr)) for attr in obj.field_names.keys() if attr != obj.id_attr]
            
            self.rbuttons[-1].grid(row=idx+1, column=0)
            for i, lbl in enumerate(entry):
                lbl.grid(row=idx+1, column=i+1)

            self.tbl_elems.append(entry)
        
        last_row = len(objs) + 8

        self.btn_del.grid(row=last_row, column=0)
        self.btn_back.grid(row=last_row, column=1)

