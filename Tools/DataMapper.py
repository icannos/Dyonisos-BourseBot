__author__ = 'ValadeAurelien'

import os
import sqlite3 as sq
import sys
reload(sys)
sys.setdefaultencoding("utf-8")



class DataMapper():
    """Short DataMapper with some functions.
    Called in the rest of Dyonisos BourseBot, it can be turned into a DataMapper made for MySql."""
    database_name, database_path = None, None
    connexion, cursor, description, header = None, None, None, None
    tables = None

    def __init__(self, database_name, database_path):
        """Void: initialization of the connexion, which is established here."""
        self.database_name = database_name
        self.database_path = database_path
        self.establish_connexion()

    def commit_n_close(self):
        """Void: commits then closes the connexion."""
        self.commit()
        self.connexion.close()

    def establish_connexion(self):
        """Void: establishes the connexion to given database."""
        try:
            self.connexion = sq.connect(self.database_path + r'\\ '[0] + self.database_name)
            self.cursor = self.connexion.cursor()
        except sq.Error as error:
            raise SystemError('SQLite error: ' + error[0])

    def commit(self):
        """Void: commits."""
        self.connexion.commit()

    def execute(self, order, params={}):
        """
        :param order: SQL string with the request to execute
        :param params: Parameters wich are in the SQL String noted ":param", Parameters is a dictonary
        with the relation between parameters and notation in the string: :name / {'name': var}
        Void: executes a single order.

        """
        try:
            self.cursor.execute(order, params)
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

    def get_all(self, order):
        """List of tuples: returns the fetched object of a selection."""
        self.execute(order)
        return self.fetchall()

    def get_one(self, order):
        """List of tuples?: returns the first of a list-object created by a selection order."""
        self.execute(order)
        return self.fetchone()

    def open_database_dir(self):
        """Void: opens the database folder."""
        os.startfile(self.database_path)

    def fetch_tables(self):
        """
        Fetches the list of the tables in the DB. Returns nothing. See get_tables().
        """
        self.tables = self.get_all("SELECT * FROM dbname.sqlite_master WHERE type='table'")

    def get_tables(self):
        """
        Returns the tables names of the DB.
        """
        if not self.tables:
            self.fetch_tables()
        return self.tables

