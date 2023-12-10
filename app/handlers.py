from tkinter import *

class EventHandlers:
    app_context:Tk = None

    def __init__(self, app):
        app_context = app


    def on_btn1_click(self, event):
        print(event.x, event.y)
        return