__author__ = 'Maxime'

import logging
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class GenericScript:

    scriptname = 'genericscript'
    version = '1'

    answer = []

    conf = []

    def __init__(self, conf):
        self.setconf(conf)

    def setconf(self, conf):
        self.conf = conf

    def run(self):
        raise SystemError('You have to overwrite run()')

    def logexec(self):
        logging.info(self.scriptname + ' run.')