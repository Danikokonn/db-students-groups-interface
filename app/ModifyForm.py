from .db_models import *
from tkinter import *
from tkinter.messagebox import showerror, showinfo, showwarning
from sqlalchemy import Engine, exc, select
from sqlalchemy.orm import Session, sessionmaker


class ModifyForm(Toplevel):
    def __init__(self, master, engine: Engine, cls=None, obj=None, *args, **kwargs):
        super().__init__(master)

        self.dbengine = engine

        self.session: Session = None

        self.current_class = cls

        self.current_obj = obj

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title(f"Изменение объекта {self.current_class.desc}")

        self.btn_mod = Button(self, text=f"Изменить объект {self.current_class.desc}")
        self.btn_mod.bind(
            "<ButtonRelease>",
            self.on_btn_mod_clicked,
        )

        self.btn_back = Button(self, text="Назад")
        self.btn_back.bind(
            "<ButtonRelease>",
            self.on_btn_back_clicked,
        )

        self.var_modificated = StringVar()  # модифицируемый

        self.rbuttons = []
        self.tbl_elems = []

        self.lbl_infotitle = Label(
            self, text="Форма для ввода изменений (оставить поле пустым - не изменять)"
        )

        self.lbls_head: dict[str, Label] = {}  # Метки шапки таблицы

        for k in self.current_class.field_names.keys():
            self.lbls_head[k] = Label(self, text=self.current_class.field_names[k])

        self.str_vars: dict[str, StringVar] = {}  # Строковые буферы для инпутов
        self.lbls: dict[str, Label] = {}  # Метки полей
        self.txts: dict[str, Entry] = {}  # Поля для ввода

        for k in self.current_class.field_names.keys():
            self.lbls[k] = Label(self, text=self.current_class.field_names[k])
            self.str_vars[k] = StringVar()
            self.txts[k] = Entry(self, textvariable=self.str_vars[k])

        self.after_idle(self.on_open)

    def session_manager(func):
        def wrapper(self, event=None, *args, **kwargs):
            if self.session is None or not self.session.is_active:
                self.session = sessionmaker(bind=self.dbengine)()
            try:
                func(self, event, *args, **kwargs)
            except exc.DataError as e:
                showerror(
                    "Ошибка ввода данных!", f"Проверьте корректность ввода данных!"
                )
                print(e)
            except exc.IntegrityError as e:
                if "violates foreign key" in str(e.orig):
                    showerror(
                        f"Ошибка изменения номера!",
                        "С этим объектом связаны другие объекты, номер нельзя изменить!",
                    )
                else:
                    showerror("Ошибка изменения!", e.orig)
            except IndexError:
                showerror("Ошибка!", "Объектов нет!")
                self.on_closing(event)
            except ValueError as e:
                showwarning(
                    "Изменений не произошло!",
                    "Введите изменения в соответсвующие поля!",
                )
                print(e, e.args)
            except Exception as e:
                showerror("Неизвестная ошибка!", e)
            if self.session.is_active:
                self.session.close()

        return wrapper

    @session_manager
    def on_btn_mod_clicked(self, event):
        obj = self.session.get(self.current_class, self.var_modificated.get())
        # Извлечение ввода
        input = {}
        for k in obj.field_names.keys():
            input[k] = self.str_vars[k].get()

        if not any([len(str(var)) for var in input.values()]):
            raise ValueError("all fields are empty")

        for attr in obj.field_names.keys():
            if len(input[attr]):
                setattr(obj, attr, input[attr])

        self.session.commit()

        showinfo("Операция выполнена успешно!", "Объект успешно изменён!")

        # Очистка ввода
        for k in self.current_class.field_names.keys():
            self.str_vars[k].set("")

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
        stmt = select(self.current_class).order_by(self.current_class.id)
        objs = self.session.scalars(stmt).all()
        self.tbl_elems.clear()
        self.rbuttons.clear()

        # Размещение шапки
        for idx, k in enumerate(self.current_class.field_names.keys()):
            self.lbls_head[k].grid(row=0, column=idx)

        self.var_modificated.set(objs[0].id)
        for idx, obj in enumerate(objs):
            text, value = (obj.id, obj.id)
            self.rbuttons.append(
                Radiobutton(self, text=text, value=value, variable=self.var_modificated)
            )
            entry = [
                Label(self, text=getattr(obj, attr))
                for attr in obj.field_names.keys()
                if attr != obj.id_attr
            ]

            self.rbuttons[-1].grid(row=idx + 1, column=0)
            for i, lbl in enumerate(entry):
                lbl.grid(row=idx + 1, column=i + 1)

            self.tbl_elems.append(entry)

        last_row = len(objs) + 8

        self.lbl_infotitle.grid(row=last_row - 3, columnspan=4)

        idx = 0

        for idx, k in enumerate(self.current_class.field_names.keys()):
            self.lbls[k].grid(row=last_row + idx, column=0)
            self.txts[k].grid(row=last_row + idx, column=1)

        self.btn_mod.grid(row=last_row + idx + 1, column=0)
        self.btn_back.grid(row=last_row + idx + 1, column=1)
