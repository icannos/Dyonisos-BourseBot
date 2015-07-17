__author__ = 'ValadeAurelien'


import GlobalFile
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class ExecuteAdvice():
    """
     Writes new lines in system_firms_marks.database.db .
    It considers a single piece of advice and modified by rewritting the infos about the firm concerned by this piece of advice
     """
    DataM = None
    advice = None
    module_mark = None
    firm_infos = None

    def __init__(self, advice):
        """
        Writes in the database, as soon as defined.
        Package = (module_name, module_answer) .
        """
        self.DataM = GlobalFile.get_DataMapper()
        self.advice = advice

    def fetch_module_mark(self):
        """
        Fetches the marks of the considered module in system_modules_marks.database.db .
        """
        self.module_mark = self.DataM.get_one("SELECT markS,markM,markL FROM system_modules_marks WHERE name='" + self.advice.module_name + "'")
        if not self.module_mark:
            self.module_mark = (1, 1, 1)

    def fetch_firm_infos(self):
        """
        Fetches the datas of the considered firm in system_firms_marks.database.db .
        """
        self.firm_infos = self.DataM.get_one("SELECT * FROM system_firms_marks WHERE isin = ' " + self.advice.firm_isin + " ' ORDER BY id DESC LIMIT 1")
        if not self.firm_infos:
            self.firm_infos = [None, self.advice.firm_isin, 0, 0, 0, 0, 0, 0, '', None]

    def execute_advice(self):
        """
        Modifies the datas of the firm in order to create a new line in the DB.
        """
        self.fetch_firm_infos()
        self.fetch_module_mark()
        actionS = self.module_mark[0]/100 * self.advice.action
        actionM = self.module_mark[1]/100 * self.advice.action
        actionL = self.module_mark[2]/100 * self.advice.action
        #firm_infos = (id, ISIN, markS, markM, markL, actionS, actionM, actionL, source, date)
        self.firm_infos[0] = None
        self.firm_infos[2] += actionS
        self.firm_infos[3] += actionM
        self.firm_infos[4] += actionL
        self.firm_infos[5] = actionS
        self.firm_infos[6] = actionM
        self.firm_infos[7] = actionL
        self.firm_infos[8] = self.advice.module_name.encode('utf-8')
        self.firm_infos[9] = time.time()
        return self.firm_infos


class FirmsMarksWriter():

    DataM = None
    g_modules_packages = None

    def __init__(self, g_modules_packages):
        """
        Updates the database by creating new lines based on the modules answers and their marks stored in the DB.
        The changes are committed.
        package = [(mod.answer)...]
        mod.answer = [advice...]
        unpacked generator= [advice...] (of every modules)
        advice = advice object
        """
        self.DataM = GlobalFile.get_DataMapper()
        self.g_modules_packages = g_modules_packages
        self.execute_answers()
        self.DataM.commit()

    def g_unpack(self):
        for mod in self.g_modules_packages:
            for advice in mod:
                yield advice
        raise (StopIteration)

    def g_new_f_infos(self):
        for advice in self.g_unpack():
            update = ExecuteAdvice(advice)
            yield update.execute_advice()
        raise (StopIteration)

    def execute_answers(self):
        """
        Calls an object that makes the execution for each module.
        """
        self.DataM.executemany('INSERT INTO system_firms_marks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [item for item in self.g_new_f_infos()])
