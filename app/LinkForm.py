from .db_models import *
from tkinter import *
from tkinter.messagebox import showerror, showinfo, showwarning
from sqlalchemy import Engine, exc, select
from sqlalchemy.orm import Session, sessionmaker

class LinkForm(Toplevel):
    def __init__(self, master, engine:Engine, cls1, cls2, *args, **kwargs):
        super().__init__(master)
        
        self.dbengine = engine

        self.session:Session = None

        self.cls1 = cls1
        self.cls2 = cls2

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title(f"Связывание объектов {self.cls1.desc}, {self.cls2.desc}")

        self.f_head = Frame(self) # Фрейм заголовка
        self.f_obj1 = Frame(self) # Фрейм объекта 1
        self.f_obj2 = Frame(self) # Фрейм объекта 1
        self.f_bot = Frame(self)  # Фрейм кнопки

        self.f_head.pack(side=TOP, expand=1, fill=BOTH, pady=10)
        self.f_obj1.pack(side=TOP, expand=1, fill=X, pady=10)
        self.f_obj2.pack(side=TOP, expand=1, fill=X, pady=10)
        self.f_bot.pack(side=TOP, expand=1, pady=10)

        self.btn_mod = Button(self.f_bot, text=f"Связать")
        self.btn_mod.bind("<ButtonRelease>", self.on_btn_link_clicked,)

        self.btn_back = Button(self.f_bot, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked,)

        self.var1 = StringVar() # связываемый 1
        self.var2 = StringVar() # связываемый 2
        

        self.f_col1 = [Frame(self.f_obj1) for _ in range(len(self.cls1.field_names.keys()))] # фрейм-колонка
        self.rbuttons1 = []
        self.tbl_elems1 = []

        for f in self.f_col1:
            f.pack(side=LEFT, expand=1, fill=X, padx=15)

        self.f_col2 = [Frame(self.f_obj2) for _ in range(len(self.cls2.field_names.keys()))] # фрейм-колонка
        self.rbuttons2 = []
        self.tbl_elems2 = []

        for f in self.f_col2:
            f.pack(side=LEFT, expand=1, fill=X, padx=15)

        self.lbls_head1:dict[str, Label] = {} # Метки шапки таблицы 1
        self.lbls_head2:dict[str, Label] = {} # Метки шапки таблицы 2

        self.after_idle(self.on_open)


    def session_manager(func):
        def wrapper(self, event=None, *args, **kwargs):
            if self.session is None or not self.session.is_active:
                self.session = sessionmaker(bind=self.dbengine)()
            try:
                func(self, event, *args, **kwargs)
            except exc.DataError as e:
                showerror("Ошибка ввода данных!", f"Проверьте корректность ввода данных!")
                print(e)
            except exc.IntegrityError as e:
                if "violates foreign key" in str(e.orig):
                    showerror(f"Ошибка изменения номера!", "С этим объектом связаны другие объекты, номер нельзя изменить!")
                else:
                    showerror("Ошибка изменения!", e.orig)
                    print(e)
            except IndexError:
                showerror("Ошибка!", "Объектов нет!")
                self.on_closing(event)
            except ValueError as e:
                showwarning("Изменений не произошло!", "Введите изменения в соответсвующие поля!")
                print(e, e.args)
            except Exception as e:
                showerror("Неизвестная ошибка!", e.args)
                print(e)
            if self.session.is_active:
                self.session.close()
        return wrapper


    @session_manager
    def on_btn_link_clicked(self, event):
        obj1 = self.session.get(self.cls1, self.var1.get())
        obj2 = self.session.get(self.cls2, self.var2.get())

        fld1 = obj1.linked_fields[obj2.__class__.__name__]
        fld2 = obj2.linked_fields[obj1.__class__.__name__]

        match(obj1.link_types[fld1]):
            case "one_to_many":
                getattr(obj1, fld1).append(obj2)
                setattr(obj2, fld2, obj1)
            case "one_to_one":
                setattr(obj1, fld1, obj2)
                setattr(obj2, fld2, obj1)
            case "many_to_many":
                getattr(obj1, fld1).append(obj2)
                getattr(obj2, fld2).append(obj1)

        self.session.commit()
        
        showinfo("Операция выполнена успешно!", "Объекты связаны!")

        for widget in self.winfo_children():
            widget.grid_forget()

        self.on_open()

        
        

    def on_btn_back_clicked(self, event):
        self.on_closing(event)


    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()

    
    @session_manager
    def on_open(self, event=None):
        stmt1 = select(self.cls1).order_by(self.cls1.id)
        objs1 = self.session.scalars(stmt1).all()

        stmt2 = select(self.cls2).order_by(self.cls2.id)
        objs2 = self.session.scalars(stmt2).all()

        self.tbl_elems1.clear()
        self.rbuttons1.clear()

        self.tbl_elems2.clear()
        self.rbuttons2.clear()

        # Размещение шапки
        for idx, k in enumerate(self.cls1.field_names.keys()):
            self.lbls_head1[k] = Label(self.f_col1[idx], text=self.cls1.field_names[k])
            self.lbls_head1[k].pack(side=TOP, expand=1, pady=5)


        self.var1.set(objs1[0].id)
        for obj in objs1:
            text, value = (obj.id, obj.id)
            self.rbuttons1.append(Radiobutton(self.f_col1[0], text=text, value=value, variable=self.var1))
            entry = [ Label(self.f_col1[idx], text=getattr(obj, attr)) for idx, attr in enumerate(obj.field_names.keys()) if attr != obj.id_attr]
            
            self.rbuttons1[-1].pack(side=TOP, expand=1, pady=5)
            for i, lbl in enumerate(entry):
                lbl.pack(side=TOP, expand=1, pady=5)

            self.tbl_elems1.append(entry)


        # Размещение шапки
        for idx, k in enumerate(self.cls2.field_names.keys()):
            self.lbls_head2[k] = Label(self.f_col2[idx], text=self.cls2.field_names[k])
            self.lbls_head2[k].pack(side=TOP, expand=1, pady=5)

        self.var2.set(objs2[0].id)
        for idx, obj in enumerate(objs2):
            fld = obj.linked_fields[objs1[0].__class__.__name__]
            if obj.link_types[fld] in ["many_to_one", "one_to_one"]:
                continue
            text, value = (obj.id, obj.id)
            self.rbuttons2.append(Radiobutton(self.f_col2[0], text=text, value=value, variable=self.var2))
            entry = [ Label(self.f_col2[idx], text=getattr(obj, attr)) for idx, attr in enumerate(obj.field_names.keys()) if attr != obj.id_attr]
            
            self.rbuttons2[-1].pack(side=TOP, expand=1, pady=5)
            for i, lbl in enumerate(entry):
                lbl.pack(side=TOP, expand=1, pady=5)

            self.tbl_elems2.append(entry)

        self.btn_mod.pack(side=LEFT, expand=1, fill=X, padx=15)
        self.btn_back.pack(side=LEFT, expand=1, fill=X, padx=15)

