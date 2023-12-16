from .db_models import *
from tkinter import *
from tkinter.ttk import Treeview, Scrollbar
from tkinter.messagebox import showerror, showinfo, showwarning
from sqlalchemy import Engine, exc, select
from sqlalchemy.orm import Session, sessionmaker

class TreeViewRead(Toplevel):
    def __init__(self, master, engine:Engine):
        super().__init__(master)
        
        self.dbengine = engine

        self.nodes = {}

        self.session:Session = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Просмотр данных")

        self.tree_view = Treeview(self)
        self.tree_view.heading("#0", text="База данных группы-студенты", anchor=W)

        self.ysb = Scrollbar(self, orient=VERTICAL,
                            command=self.tree_view.yview)
        self.xsb = Scrollbar(self, orient=HORIZONTAL,
                            command=self.tree_view.xview)
        self.tree_view.configure(yscroll=self.ysb.set, xscroll=self.xsb.set)


        self.tree_view.bind("<<TreeviewOpen>>", self.open_node)
        

        self.tree_view.grid(row=0, column=0, sticky=N + S + E + W)
        self.ysb.grid(row=0, column=1, sticky=N + S)
        self.xsb.grid(row=1, column=0, sticky=E + W)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.btn_back = Button(self, text="Назад")
        self.btn_back.bind("<ButtonRelease>", self.on_btn_back_clicked,)

        self.session = sessionmaker(bind=self.dbengine)()
        stmt = select(Faculty).order_by(Faculty.id)
        rows = self.session.scalars(stmt).all()

        self.populate_node("", rows)
        

    def on_btn_back_clicked(self, event):
        self.on_closing(event)


    def on_closing(self, event=None):
        self.master.deiconify()
        self.destroy()

    
    def populate_node(self, parent, rows):
        for entry in rows:
            node = self.tree_view.insert(parent, END, text=entry.get_name(), open=False)
            keys =  entry.refs.keys()
            self.nodes[node] = []
            for key in keys:
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
        

        