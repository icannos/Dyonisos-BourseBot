__author__ = 'Maxime'

import logging
import GlobalFile
import sys
reload(sys)
sys.setdefaultencoding("utf-8")



class advice:
    mod_name = None
    action = 0 #Must Take 0,1 or -1
    date = None
    Source = None #Used by the module to save some info


class AdviceGenericScript:

    script_name = None
    version = '1'
    DataM = None
    answer = []

    conf = []

    def __init__(self, conf):
        self.script_name = self.__class__.__name__
        self.set_conf(conf)
        self.DataM = GlobalFile.get_DataMapper()

    def set_conf(self, conf):
        self.conf = conf

    def advice_generator(self, firm):
# firm (name = 0, isin=1, code=2)
        raise SystemError('You have to overwrite advicegenerator()')

    def build_answer_generator(self, firms):
        for f in firms:
            yield(self.advice_generator(f))

    def run(self, firms):
        self.answer = self.build_answer_generator(firms)
        return self.answer

    def logexec(self):
        logging.info(self.script_name + ' run.')

