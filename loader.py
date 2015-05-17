
import logging
import sys
import Tools.DataMapper as DM
reload(sys)
sys.setdefaultencoding("utf-8")


class Loader:

    datam = None

    def __init__(self, DataMapper):
        self.datam = DataMapper

    def load_modules(self):

        # name = 0, active = 1, block = 2
        self.datam.execute('SELECT name, active, block FROM system_modules WHERE active=1')
        modules = self.datam.fetchall()

        modulesok = []

        for m in modules:
            try:
                modulesok.append([str(m[2]), str(m[0]), __import__(m[2] + "." + m[0], globals(), locals(), [m[0]], -1)])
                logging.info( str(m[2]) + "." + str(m[0]) + ": Charge.")

            except ImportError:
                logging.warning( str(m[2]) + "." + str(m[0]) + ": Echec.")

        return modulesok


    def load_configuration(self):
        #name = 0, value = 1
        self.datam.execute('SELECT name, value FROM system_configuration')
        conf = self.datam.fetchall()
        confok = {}

        for c in conf:
            confok[c[0]] = c[1]
            logging.info( str(str(c[0]) + ": Charge."))

        return confok


#function called only when reloading: builds the table of the firms cotted at Paris trade agency
    def save_firms(self, firms):
        listfirms = []
        for l in firms:
            listfirms.append((l['FirmName'], l['FirmISIN'], l['FirmCode']))

        self.datam.executemany('INSERT INTO system_firms (name, isin, code) VALUES (?, ?, ?)', listfirms)
        self.datam.commit_n_close()


if __name__ == '__main__':
    l = Loader()
    l.load_modules()