import sqlite3
import pandas as pd


class TwitterDatabase(object):

    __column_names__ = [
        'id', 'conversation_id', 'date', 'time', 'timezone', 'username', 
        'tweet', 'replies_count', 'retweets_count', 'likes_count', 'link'
    ]

    def __init__(self, database_name, table_name):
        self.connect(database_name)
        self.create_table(table_name)

    def insert(self, item, table_name):
        self.cursor.execute(
            f"INSERT OR IGNORE INTO {table_name} VALUES(?,?,?,?,?,?,?,?,?,?,?)", item
        )
        self.connection.commit()

    def read(self, table_name, columns=None, to_pandas=False):
        if columns is None:
            self.cursor.execute(
                f"SELECT * FROM {table_name}"
            )
            columns = self.__column_names__
        else:
            self.cursor.execute(
                f"SELECT {', '.join(columns)} FROM {table_name}"
            )
        rows = self.cursor.fetchall()
        if to_pandas:
            return pd.DataFrame(rows, columns=columns)
        return rows

    def connect(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name):
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name}("
            f"  id INTEGER PRIMARY KEY, "
            f"  conversation_id INTEGER, "
            f"  date TEXT, "
            f"  time TEXT, "
            f"  timezone TEXT, "
            f"  username TEXT, "
            f"  tweet TEXT, "
            f"  replies_count INTEGER, "
            f"  retweets_count INTEGER, "
            f"  likes_count INTEGER, "
            f"  link TEXT"
            f")"
        )
        self.connection.commit()

    def drop_table(self, table_name):
        self.cursor.execute(f"DROP TABLE {table_name}")
