__author__ = 'ValadeAurelien'

import os
import sqlite3 as sq


class DataMapper():
    """Short DataMapper with some functions.
    Called in the rest of Dyonisos BourseBot, it can be turned into a DataMapper made for MySql."""
    database_name, database_path = None, None
    connection, cursor, description, header = None, None, None, None

    def __init__(self, database_name, database_path):
        """Void: initialization of the connection, which is established here."""
        self.database_name = database_name
        self.database_path = database_path
        self.establish_connection()

    def commit_n_close(self):
        """Void: commits then closes the connection."""
        self.commit()
        self.connection.close()

    def establish_connection(self):
        """Void: establishes the connection to given database."""
        try:
            self.connection = sq.connect(self.database_path + r'\\ '[0] + self.database_name)
            self.cursor = self.connection.cursor()
        except sq.Error as error:
            raise SystemError('SQLite error: ' + error[0])

    def commit(self):
        """Void: commits."""
        self.connection.commit()

    def execute(self, order):
        """Void: executes a single order."""
        try:
            self.cursor.execute(order)
        except sq.Error as error:
            raise SystemError('SQLite error: ' + error[0])

    def executemany(self, order, arglist):
        """Void: executes a many orders. The second argument has to be a list (or bigger like a table)."""
        try:
            self.cursor.executemany(order, arglist)
        except sq.Error as error:
            raise SystemError('SQLite error: ' + error[0])

    def fetchone(self):
        """Tuple: returns the value of the first item of the current cursor."""
        try:
            return self.cursor.fetchone()
        except sq.Error as error:
            raise SystemError('SQLite error: ' + error[0])

    def fetchmany(self, size):
        """List of tuples: returns the values of the first items of the current cursor."""
        try:
            return self.cursor.fetchmany(size)
        except sq.Error as error:
            raise SystemError('SQLite error: ' + error[0])

    def fetchall(self):
        """List of tuples: returns all the values of the current cursor."""
        try:
            return self.cursor.fetchall()
        except sq.Error as error:
            raise SystemError('SQLite error: ' + error[0])

    def get_description(self):
        """List of tuples: returns and builds the current cursor description.
        [(header1, ?, ?, .....), (header2, ?, ?, .....), .....].
        shapes = (line = nb of columns of the SQL table | column = nb of rows of the SQL table)."""
        try:
            self.description = self.cursor.description
            return self.description
        except sq.Error as error:
            raise SystemError('SQLite error: ' + error[0])

    def get_header(self):
        """List of strings: returns and builds the headers of the current selection. UTF-8 objects are encoded."""
        self.get_description()
        self.header = []
        try:
            for item in self.description:
                try:
                    self.header.append(item[0].encode('utf-8'))
                except:
                    pass
            return self.header
        except:
            raise AttributeError('No header available')

    def open_database_dir(self):
        """Void: opens the database folder."""
        os.startfile(self.database_path)

