from .db_models import *
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from sqlalchemy import Engine, exc
from sqlalchemy.orm import Session, sessionmaker

class CreateForm(Toplevel):
    def __init__(self, master, engine:Engine, cls):
        super().__init__(master)
        
        self.dbengine = engine

        self.session:Session = None

        self.current_class = cls

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title(f"Формирование объекта {self.current_class.desc}")

        self.str_vars:dict[str, StringVar] = {} # Строковые буферы для инпутов
        self.lbls:dict[str, Label] = {} # Метки полей
        self.txts:dict[str, Entry] = {} # Поля для ввода
        
        idx=0

        for idx, k in enumerate(self.current_class.field_names.keys()):
            self.lbls[k] = Label(self, text=self.current_class.field_names[k])
            self.lbls[k].grid(row=idx, column=0)

            self.str_vars[k] = StringVar()

            self.txts[k] = Entry(self, textvariable=self.str_vars[k])
            self.txts[k].grid(row=idx, column=1)

        self.btn_create = Button(self, text=f"Создать объект {self.current_class.desc}")
        self.btn_create.bind("<ButtonRelease>", self.on_btn_add_clicked)
        self.btn_create.grid(row=idx+1,column=0)

        self.btn_back = Button(self, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked)
        self.btn_back.grid(row=idx+1,column=1)


    def session_manager(func):
        def wrapper(self, event, *args, **kwargs):
            if self.session is None or not self.session.is_active:
                self.session = sessionmaker(bind=self.dbengine)()
            try:
                func(self, event, *args, **kwargs)
                showinfo("Операция выполнена успешно!", "Объект успешно создан!")
            except exc.DataError:
                showerror("Ошибка ввода данных!", "Проверьте корректность ввода данных!")
            except exc.IntegrityError as e:
                if "is not present in table" in str(e.orig):
                    showerror(f"Ошибка создания!", "Попытка создать объект, связанный с несуществующим объектом!")
                else:
                    showerror("Ошибка создания!", "Объект с данным номером уже существует!")
                print(e, e.orig)
            except Exception as e:
                showerror("Неизвестная ошибка!", e.args)
                print(e, e.args)
            if self.session.is_active:
                self.session.close()
        return wrapper


    @session_manager
    def on_btn_add_clicked(self, event):
        # Извлечение ввода
        input = {}
        for k in self.current_class.field_names.keys():
            input[k] = self.str_vars[k].get()

        # Вставка записи
        obj = self.current_class()
        for attr in self.current_class.field_names.keys():
            setattr(obj, attr, input[attr])

        self.session.add(obj)
        self.session.commit()

        # Очистка ввода
        for k in self.current_class.field_names.keys():
            self.str_vars[k].set('')
        
    def on_btn_back_clicked(self, event):
        self.on_closing(event)

    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()

