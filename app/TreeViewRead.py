from .db_models import *
from tkinter import *
from tkinter.ttk import Treeview, Scrollbar
from sqlalchemy import Engine, exc, select
from sqlalchemy.orm import Session, sessionmaker


class TreeViewRead(Toplevel):
    def __init__(self, master, engine: Engine, cls, obj=None, cls2=None):
        super().__init__(master)

        self.dbengine = engine

        self.nodes = {}

        self.session: Session = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Просмотр данных")

        self.current_cls = cls

        self.current_obj = obj

        self.f_head = Frame(self)
        self.f_view = Frame(self)
        self.f_bot = Frame(self)

        self.f_head.pack(side=TOP, fill=X, pady=5)
        self.f_view.pack(side=TOP, expand=1, fill=BOTH, pady=5)
        self.f_bot.pack(side=TOP, fill=X, pady=5)

        self.lbl_head = Label(self.f_head, text="Окно просмотра")
        self.lbl_head.pack(side=TOP, expand=1)

        self.subframe1 = Frame(self.f_view)
        self.subframe2 = Frame(self.f_view)
        self.subframe1.pack(side=LEFT, fill=BOTH, expand=1)
        self.subframe2.pack(side=LEFT, fill=Y)

        self.tree_view = Treeview(self.subframe1)
        self.tree_view.heading("#0", text="База данных группы-студенты", anchor=W)

        self.ysb = Scrollbar(
            self.subframe2, orient=VERTICAL, command=self.tree_view.yview
        )
        self.xsb = Scrollbar(
            self.subframe1, orient=HORIZONTAL, command=self.tree_view.xview
        )
        self.tree_view.configure(yscroll=self.ysb.set, xscroll=self.xsb.set)

        self.tree_view.bind("<<TreeviewOpen>>", self.open_node)

        self.tree_view.pack(side=TOP, expand=1, fill=BOTH)
        self.xsb.pack(side=BOTTOM, fill=X)
        self.ysb.pack(side=LEFT, fill=Y)

        self.btn_back = Button(self.f_bot, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked)
        self.btn_back.pack(side=LEFT)

        self.session = sessionmaker(bind=self.dbengine)()

        if self.current_obj is not None:
            rows = [
                self.session.get(self.current_cls, self.current_obj.id),
            ]
        else:
            stmt = select(self.current_cls).order_by(self.current_cls.id)
            rows = self.session.scalars(stmt)

        self.populate_node("", rows)

    def on_btn_back_clicked(self, event):
        self.on_closing(event)

    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()

    def populate_node(self, parent, rows):
        for entry in rows:
            if entry.have_name:
                node = self.tree_view.insert(
                    parent, END, text=entry.get_name(), open=False
                )
            else:
                for v in entry.get_values():
                    node = self.tree_view.insert(parent, END, text=v, open=False)
            self.nodes[node] = []
            for key in entry.refs:
                if len(getattr(entry, key)):
                    self.nodes[node].append(getattr(entry, key))
                    self.tree_view.insert(node, END)

    def open_node(self, event):
        item = self.tree_view.focus()
        leafs = self.nodes.pop(item, False)
        if leafs:
            children = self.tree_view.get_children(item)
            self.tree_view.delete(children)
            for l in leafs:
                self.populate_node(item, l)
