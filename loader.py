import sqlite3
import logging

class Loader:

    def connexion(self):
        return sqlite3.connect('data/database.db')

    def loadmodules(self):
        conn = self.connexion()

        # name = 0, active = 1, fonction = 2
        modules = conn.execute('SELECT name, active, fonction FROM system_modules WHERE active=1 ').fetchall()

        modulesok = []

        for m in modules:
            try:
                modulesok.append([str(m[2]), str(m[0]), __import__(m[2] + "." + m[0], globals(), locals(), [m[0]], -1)])
                logging.info( str(m[2]) + "." + str(m[0]) + ": Charge.")

            except ImportError:
                logging.warning( str(m[2]) + "." + str(m[0]) + ": Echec.")

        return modulesok


    def loadconfiguration(self):
        #name = 0, value = 1
        conn = self.connexion()
        conf = conn.execute('SELECT name, value FROM system_configuration').fetchall()
        confok = {}

        for c in conf:
            confok[c[0]] = c[1]
            logging.info( str(str(c[0]) + ": Charge."))

        return confok

if __name__ == '__main__':
    l = Loader()
    l.loadmodules()