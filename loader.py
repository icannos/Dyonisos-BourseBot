import sqlite3
import logging
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


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


# Fonction utilisée normalement qu'au moment d'un reload ou à la 1ere utilisation pour charger la liste des entreprises côtées à Paris
    def savefirms(self, firms):
        listfirms = []
        for l in firms:
            listfirms.append((l['FirmName'], l['FirmISIN'], l['FirmCode']))

        conn = self.connexion()

        conn.executemany('INSERT INTO system_firms (name, isin, code) VALUES (?, ?, ?)', listfirms)
        conn.commit()
        conn.close()


if __name__ == '__main__':
    l = Loader()
    l.loadmodules()