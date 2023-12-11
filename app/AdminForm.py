from .CreateFaculty import *

class AdminForm(Toplevel):
    def __init__(self, master, engine:Engine):
        super().__init__(master)

        self.dbengine=engine

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.geometry("300x200")
        self.title("Окно администратора")


        self.btn_goto_create_faculty = Button(self, text="Создание факультета")
        self.btn_goto_create_faculty.bind("<ButtonRelease>", self.on_btn_goto_create_faculty_click)
        self.btn_goto_create_faculty.place(x=50, y=50)


    def on_btn_goto_create_faculty_click(self, event):
        self.withdraw()
        window = CreateFaculty(self, self.dbengine)
        window.grab_set()


    def on_closing(self):
        self.master.deiconify()
        self.destroy()

