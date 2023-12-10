import psycopg2


class Document:
    pass


class Student:
    pass


class Speciality:
    pass


class Curator:
    pass


class Groups:
    pass


class Department:
    pass


class Faculty:
    pass


class PSQL_groups_students_db:
    connection = None

    def __init__(self, host="localhost", port=3239, database="postgres", user="admin", password="psltest"):
        self.connection = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)


    def create_group():
        pass


    def delete_group():
        pass


    def add_student():
        pass


    def remove_student():
        pass


    def transfer_student


    '''
    Получить список компонентов
    Возвращает список компонентов (список строк)
    '''
    def get_components(self):
        components:list[str] = None
        sql = "SELECT DISTINCT component_name FROM etl.components"
        try:
            cur = self.connection.cursor()
            cur.execute(sql)
            components = [t[0] for t in cur.fetchall()]
        except psycopg2.DatabaseError as exc:
            print(exc)
        return components


    '''
    Получить имя компонента по полному имени файла
    Возвращает имя компонента (строку)
    '''
    def get_component_by_fullpath(self, fullpath:str):
        component:str = None
        sql = f"SELECT component_name FROM etl.files WHERE full_path='{fullpath}' LIMIT 1"
        try:
            cur = self.connection.cursor()
            cur.execute(sql)
            component = cur.fetchone()[0]
        except psycopg2.DatabaseError as exc:
            print(exc)
        return component


    '''
    Получить список файлов для выбранного компонента (весь список, если не указывать компонент)
    Возвращает список словарей (название столбца в бд: значение), содержащих информацию о файле 
    '''
    def get_files_info_list(self, component:str=None):
        try:
            sql = "SELECT DISTINCT full_path, filename, filepath, filetype FROM etl.files" + (f" WHERE component_name='{component}'" if component else "")
            cur = self.connection.cursor()
            cur.execute(sql)
            head = tuple([col.name for col in cur.description])
            file_info = [dict(zip(head, file)) for file in cur.fetchall()]
            return file_info
        except psycopg2.DatabaseError as exc:
            print(exc)



    '''
    Получить список полных названий файлов для выбранного компонента (весь список, если не указывать компонент)
    Возвращает список полных имён файлов
    '''
    def get_files_fullpaths(self, component:str=None):
        files:list[str] = None
        sql = "SELECT DISTINCT full_path FROM etl.files" + (f" WHERE component_name='{component}'" if component else "")
        try:
            cur = self.connection.cursor()
            cur.execute(sql)
            files = [t[0] for t in cur.fetchall()]
        except psycopg2.DatabaseError as exc:
            print(exc)
        return files


    '''
    Получить список параметров для выбранного компонента
    Возвращает список словарей (название столбца в бд: значение), содержащих информацию о параметре
    '''
    def get_artifacts_by_component(self, component:str):
        try:
            sql = f"""
                SELECT DISTINCT par_name, value, schema::text, p.full_path
                FROM etl.parameters p 
                INNER JOIN etl.files f 
                ON p.full_path=f.full_path 
                WHERE f.component_name='{component}'
            """
            cur = self.connection.cursor()
            cur.execute(sql)
            head = tuple([col.name for col in cur.description])
            params = [dict(zip(head, param)) for param in cur.fetchall()]
            return params
        except psycopg2.DatabaseError as exc:
            print(exc)


    '''
    Получить список параметров для выбранного файла
    Возвращает список словарей (название столбца в бд: значение), содержащих информацию о параметре
    '''
    def get_artifacts_by_fullpath(self, fullpath:str):
        try:
            sql = f"""
                SELECT DISTINCT par_name, value, schema::text, full_path
                FROM etl.parameters
                WHERE full_path='{fullpath}'
            """
            cur = self.connection.cursor()
            cur.execute(sql)
            head = tuple([col.name for col in cur.description])
            params = [dict(zip(head, param)) for param in cur.fetchall()]
            return params
        except psycopg2.DatabaseError as exc:
            print(exc)






artifact_db = PSQL_artifact_db()

print(artifact_db.get_components())

print(artifact_db.get_files_info_list(artifact_db.get_components()[0]))

print(artifact_db.get_files_fullpaths(artifact_db.get_components()[0]))

print(artifact_db.get_artifacts_by_component(artifact_db.get_components()[0]))

print(artifact_db.get_artifacts_by_fullpath(artifact_db.get_files_fullpaths(artifact_db.get_components()[0])[0]))

print(artifact_db.get_component_by_fullpath(artifact_db.get_files_fullpaths()[0]))