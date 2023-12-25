from app.MainForm import MainForm


DBENGINE = 'postgresql+psycopg2'
DBLOGIN = 'admin'
DBPASSWORD = 'psltest'
DBHOST = 'localhost'
DBPORT = '32321'
DBNAME = 'postgres'
DBSCHEMA = 'accounting'


if __name__=="__main__":
    app = MainForm(DBENGINE, DBLOGIN, DBPASSWORD, DBHOST, DBPORT, DBNAME, DBSCHEMA)
    app.mainloop()


    