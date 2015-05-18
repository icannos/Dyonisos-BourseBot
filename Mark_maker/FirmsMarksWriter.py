__author__ = 'ValadeAurelien'


import GlobalFile
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class SingleModule():
    """
     Writes new lines in system_firms_marks.database.db .
     For a single module, each advice is written, for every firm considered by this module.
     """
    module_name, answer = None, None
    module_mark = None
    DataM = None

    def __init__(self, package):
        """
        Writes in the database, as soon as defined.
        Package = (module_name, module_answer) .
        """
        self.DataM = GlobalFile.get_DataMapper()
        self.module_name = package[0]
        self.answer = package[1]
        self.fetch_module_mark()
        self.execute_answer()

    def fetch_module_mark(self):
        """
        Fetches the marks of the considered module in system_modules_marks.database.db .
        """
        self.module_mark = self.DataM.get_all('SELECT (markS,markM,markL) FROM system_modules_marks WHERE name = ' + self.module_name)

    def fetch_firm_infos(self, firm_name):
        """
        Fetches the datas of the considered firm in system_firms_marks.database.db .
        """
        return self.DataM.get_all('SELECT * FROM system_firms_marks WHERE name = ' + firm_name + ' ORDER BY id DESC LIMIT 1')

    def update_firm_info(self, advice):
        """
        Modifies the datas of the firm in order to create a new line in the DB.
        """
        actionS = self.module_mark[0]/100 * advice[1]
        actionM = self.module_mark[1]/100 * advice[1]
        actionL = self.module_mark[2]/100 * advice[1]
        firm_infos = self.fetch_firm_infos(advice[0])
        #firm_infos = (id, ISIN, markS, markM, markL, actionS, actionM, actionL, source, date)
        firm_infos[2] += actionS
        firm_infos[3] += actionM
        firm_infos[4] += actionL
        firm_infos[5] = actionS
        firm_infos[6] = actionM
        firm_infos[7] = actionL
        firm_infos[8] = self.module_name
        firm_infos[9] = time.time()
        firm_infos.pop(0)
        return firm_infos

    def gene_module_advices(self):
        """
        Builds a generator which returns at each iteration a tuple: the infos of the firm considered.
        """
        for advice in self.answer:
            yield self.update_firm_info(advice)
        raise StopIteration

    def execute_answer(self):
        """
        An executemany() executes all the advices of an answer (ie a module answer).
        """
        self.DataM.executemany('INCLUDE INTO sys_firms_marks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', self.gene_module_advices())


class FirmsMarksWriter():

    g_modules_packages = None

    def __init__(self, g_modules_packages):
        """
        Updates the database by creating new lines based on the modules answers and their marks stored in the DB.
        The changes are committed.
        """
        self.DataM = GlobalFile.get_DataMapper()
        self.g_modules_packages = g_modules_packages
        self.execute_answers()
        self.DataM.commit()

    def execute_answers(self):
        """
        Calls an object that makes the execution for each module.
        """
        for answer in self.g_modules_packages:
            SingleModule(answer)

