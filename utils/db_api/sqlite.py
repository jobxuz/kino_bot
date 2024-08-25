import sqlite3


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self,chat_id: int, first_name: str,username: str ,date: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO users(chat_id,first_name ,username, date) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(chat_id,first_name,username,date), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM users;", fetchone=True)

    def update_user_lang(self, lang, chat_id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE users SET lang=? WHERE chat_id=?
        """
        return self.execute(sql, parameters=(lang, chat_id), commit=True)


    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


    def delete_channels(self,**kwargs):
        sql = """

        DELETE  FROM channels where
        
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters,commit=True)


    def add_channels(self,chat_id: str, name: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO channels(chat_id,name) VALUES(?, ?)
        """
        return self.execute(sql, parameters=(chat_id,name), commit=True)

    def select_all_channels(self):
        sql = """
        SELECT * FROM channels
        """
        return self.execute(sql, fetchall=True)
    

    def add_kino(self,cod: int, file_id: str, name: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO video(cod,file_id,name) VALUES(?, ?, ?)
        """
        return self.execute(sql, parameters=(cod,file_id,name), commit=True)
    

    def select_all_kino(self):
        sql = """
        SELECT * FROM video
        """
        return self.execute(sql, fetchall=True)
    

    def delete_video(self,**kwargs):
        sql = """

        DELETE  FROM video where
        
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters,commit=True)
    

    def select_kino(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM video WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    


def logger(statement):
    pass
#     print(f"""
# _____________________________________________________
# Executing:
# {statement}
# _____________________________________________________
# """)