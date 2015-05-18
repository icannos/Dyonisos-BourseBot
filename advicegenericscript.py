__author__ = 'Maxime'

import logging

import sys
reload(sys)
sys.setdefaultencoding("utf-8")



class AdviceGenericScript:

    script_name = None
    version = '1'

    answer = []

    conf = []

    def __init__(self, conf):
        self.script_name = self.__class__.__name__
        self.set_conf(conf)

    def set_conf(self, conf):
        self.conf = conf


    def advice_generator(self, firm):
        raise SystemError('You have to overwrite advicegenerator()')

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

