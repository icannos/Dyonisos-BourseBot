__author__ = 'ValadeAurelien'


import GlobalFile

import logging
from MathTools import *
import sys
reload(sys)
sys.setdefaultencoding("utf-8")



class AdviceGenericScript:
    DataM = GlobalFile.get_DataMapper()
    script_name = None
    version = '1'

    answer = []

    conf = []

    def __init__(self, conf):
        self.script_name = self.__class__.__name__
        self.set_conf(conf)
        self.get = self.DataM.get_all

    def set_conf(self, conf):
        self.conf = conf

    def advice_generator(self, firm):
        raise SystemError('You have to overwrite advice_generator()')

    def build_answer_generator(self, firms):
        for f in firms:
            yield(self.advice_generator(f))

    def built_answer_generator(self, firms):
        for firm in firms:
            yield(self.advice_generator(firm))

    def run(self, firms):
        self.answer = self.build_answer_generator(firms)
        return self

    def logexec(self):
        logging.info(self.script_name + ' run.')

