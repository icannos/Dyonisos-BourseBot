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
        self.setconf(conf)

    def setconf(self, conf):
        self.conf = conf

    def advicegenerator(self, f):
        raise SystemError('You have to overwrite run()')

    def built_answergenerator(self, firms):
        for f in firms:
            yield(self.advicegenerator(f))

    def run(self, firms):
        self.answer = self.built_answergenerator(firms)
        return self

    def logexec(self):
        logging.info(self.script_name + ' run.')

