__author__ = 'Maxime'

import logging
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class GenericScript:

    scriptname = 'genericscript'
    version = '1'


    conf = []

    def __init__(self, conf):
        self.setconf(conf)

    def setconf(self, conf):
        self.conf = conf

    def run(self):
        self.conf = self.conf

    def LogExec(self):
        logging.info(self.scriptname + ' run.')