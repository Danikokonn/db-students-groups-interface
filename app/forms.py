from tkinter import *
from .handlers import EventHandlers


### Doc
class Form(object):
    # form
    root: Tk = None
    eh: EventHandlers = None

    # components
    btn1: Button = None
    txtbx1 = None

    def __init__(self):

        self.root = Tk()
        self.eh = EventHandlers(self.root)

        self.btn1 = Button(self.root, text="ok")
        self.btn1.bind("<ButtonRelease>", self.eh.on_btn1_click,)
        self.btn1.place(x=50, y=50)

        self.txtbx1 = Text(self.root, width=10, height=1)
        self.txtbx1.place(y=10, x=50)

