from .CreateForm import *
from .ModifyForm import *
from .DeleteForm import *
from .LinkForm import *

class AdminForm(Toplevel):
    def __init__(self, master, engine:Engine):
        super().__init__(master)

        self.dbengine=engine

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Окно администратора")

        self.form_types = [ CreateForm, ModifyForm, DeleteForm ]
        self.op_names = [ "Создать", "Изменить", "Удалить" ]
        self.models = [ Faculty, Department, Curator, Group, Student, Passport, Speciality ]

        self.h_frame = Frame(self)
        self.f_top = Frame(self)
        self.f_bot = Frame(self)
        self.b_frame = Frame(self)

        self.h_frame.pack(side=TOP, fill=X, pady=10)
        self.f_top.pack(side=TOP, expand=1, fill=BOTH, pady=10)
        self.f_bot.pack(side=TOP, expand=1, fill=BOTH, pady=10)
        self.b_frame.pack(side=TOP, fill=X, pady=10)

        self.lbl_head = Label(self.h_frame, text="Окно администратора\nВыберите действие с каким либо объектом")
        self.lbl_head.pack(side=TOP, expand=1, fill=BOTH)

        self.btn_back = Button(self, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked)
        self.btn_back.pack(side=LEFT, expand=1, anchor=W, pady=10)

        self.frames = []

        for _ in range(4):
            self.frames.append(Frame(self.f_top))
            self.frames[-1].pack(side=LEFT, expand=1, fill=X, padx=15)

        for _ in range(4):
            self.frames.append(Frame(self.f_bot))
            self.frames[-1].pack(side=LEFT, expand=1, fill=X, padx=15)

        self.goto_buttons = []
        self.lbls = []

        for i, model in enumerate(self.models):
            self.lbls.append(Label(self.frames[i], text=model.desc))
            self.lbls[-1].pack(side=TOP, expand=1, fill=X)
            for j, op in enumerate(self.form_types):
                self.goto_buttons.append(Button(self.frames[i], text=self.op_names[j]))
                self.goto_buttons[-1].bind("<ButtonRelease>", lambda event, arg={"form_type": op, "cls": model}: self.on_btn_goto_click(event, arg))
                self.goto_buttons[-1].pack(side=TOP, expand=1, fill=X)

        self.lbls.append(Label(self.frames[-1], text=f"Кураторы-Группы"))
        self.lbls[-1].pack(side=TOP, expand=1, fill=X)
        self.goto_buttons.append(Button(self.frames[-1], text="Связать"))
        self.goto_buttons[-1].bind("<ButtonRelease>", lambda event, arg={"form_type": LinkForm, "cls": Curator, "cls2": Group}: self.on_btn_goto_click(event, arg))
        self.goto_buttons[-1].pack(side=TOP, expand=1, fill=X)
        self.goto_buttons.append(Button(self.frames[-1], text="Отвязать"))
        self.goto_buttons[-1].bind("<ButtonRelease>", lambda event, arg={"form_type": RemoveLinkForm, "cls": Curator, "cls2": Group}: self.on_btn_goto_click(event, arg))
        self.goto_buttons[-1].pack(side=TOP, expand=1, fill=X)

        

    def on_btn_goto_click(self, event, arg):
        self.withdraw()
        window = arg["form_type"](self, self.dbengine, cls=arg["cls"], cls2=arg["cls2"] if "cls2" in arg.keys() else None)
        window.grab_set()


    def on_btn_back_clicked(self, event):
        self.on_closing(event)


    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()

