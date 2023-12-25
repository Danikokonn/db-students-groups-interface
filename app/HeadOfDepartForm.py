from .db_models import *
from .TreeViewRead import *
from .LinkForm import *
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from sqlalchemy import Engine, exc
from sqlalchemy.orm import Session, sessionmaker


class ChooseDepartForm(Toplevel):
    def __init__(self, master, engine: Engine, *args, **kwargs):
        super().__init__(master)

        self.dbengine = engine

        self.session: Session = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title(f"Выбор кафедры")

        self.btn_confirm = Button(self, text=f"Перейти к кафедре")
        self.btn_confirm.bind(
            "<ButtonRelease>",
            self.on_btn_confirm_clicked,
        )

        self.btn_back = Button(self, text="Назад")
        self.btn_back.bind(
            "<ButtonRelease>",
            self.on_btn_back_clicked,
        )

        self.var_selected = StringVar()

        self.rbuttons = []
        self.tbl_elems = []

        self.lbls_head: dict[str, Label] = {}  # Метки шапки таблицы

        for idx, k in enumerate(Department.field_names.keys()):
            if idx > 1:
                break
            self.lbls_head[k] = Label(self, text=Department.field_names[k])
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
    def on_btn_confirm_clicked(self, event):
        obj = self.session.get(Department, self.var_selected.get())
        self.withdraw()
        window = HeadOfDepartForm(self, self.dbengine, obj)
        window.grab_set()

    def on_btn_back_clicked(self, event):
        self.on_closing(event)

    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()

    @session_manager
    def on_open(self, event=None):
        stmt = select(Department).order_by(Department.id)
        objs = self.session.scalars(stmt).all()
        self.tbl_elems.clear()
        self.rbuttons.clear()

        for idx, k in enumerate(Department.field_names.keys()):
            if idx > 1:
                break
            self.lbls_head[k].grid(row=0, column=idx)

        self.var_selected.set(objs[0].id)
        for idx, obj in enumerate(objs):
            text, value = (obj.id, obj.id)
            self.rbuttons.append(
                Radiobutton(self, text=text, value=value, variable=self.var_selected)
            )
            entry = Label(self, text=obj.full_name)

            self.rbuttons[-1].grid(row=idx + 1, column=0)
            entry.grid(row=idx + 1, column=1)

            self.tbl_elems.append(entry)

        last_row = len(objs) + 8

        self.btn_confirm.grid(row=last_row, column=0)
        self.btn_back.grid(row=last_row, column=1)


class HeadOfDepartForm(Toplevel):
    def __init__(self, master, engine: Engine, obj: Department):
        super().__init__(master)

        self.dbengine = engine

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Окно заведующего кафедрой")

        self.current_obj = obj

        self.h_frame = Frame(self)
        self.f_top = Frame(self)
        self.f_bot = Frame(self)

        self.h_frame.pack(side=TOP, fill=X, pady=10)
        self.f_top.pack(side=TOP, expand=1, fill=BOTH, pady=10)
        self.f_bot.pack(side=TOP, fill=X, pady=10)

        self.lbl_head = Label(
            self.h_frame,
            text=f"Окно заведующего кафедрой {self.current_obj.full_name}\nВыберите действие",
        )
        self.lbl_head.pack(side=TOP, expand=1, fill=X, padx=10)

        # Кнопка treeview
        self.btn_goto_treeview = Button(self.f_top, text="Просмотр данных о студентах")
        self.btn_goto_treeview.bind("<ButtonRelease>", self.on_btn_goto_treeview_click)
        self.btn_goto_treeview.pack(side=TOP, expand=1, fill=BOTH, padx=10)

        self.lbl_lnk = Label(self.f_bot, text=f"Кураторы-Группы")
        self.lbl_lnk.pack(side=TOP, expand=1, fill=X)
        self.btn_lnk = Button(self.f_bot, text="Связать")
        self.btn_lnk.bind(
            "<ButtonRelease>",
            lambda event, arg={
                "form_type": LinkForm,
                "cls": Curator,
                "cls2": Group,
            }: self.on_btn_goto_click(event, arg),
        )
        self.btn_lnk.pack(side=TOP, expand=1, fill=X)
        self.btn_ulnk = Button(self.f_bot, text="Отвязать")
        self.btn_ulnk.bind(
            "<ButtonRelease>",
            lambda event, arg={
                "form_type": RemoveLinkForm,
                "cls": Curator,
                "cls2": Group,
            }: self.on_btn_goto_click(event, arg),
        )
        self.btn_ulnk.pack(side=TOP, expand=1, fill=X)

        # Общие кнопки
        self.btn_back = Button(self.f_bot, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked)
        self.btn_back.pack(side=BOTTOM, fill=X, padx=10)

    # Обработчик treeview
    def on_btn_goto_treeview_click(self, event):
        self.withdraw()
        window = TreeViewRead(self, self.dbengine, Department, self.current_obj)
        window.grab_set()

    def on_btn_goto_click(self, event, arg):
        self.withdraw()
        window = arg["form_type"](
            self,
            self.dbengine,
            obj=self.current_obj,
            cls=arg["cls"],
            cls2=arg["cls2"] if "cls2" in arg.keys() else None,
        )
        window.grab_set()

    # Общие обработчики
    def on_btn_back_clicked(self, event):
        self.on_closing(event)

    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()
