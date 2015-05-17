__author__ = 'ValadeAurelien'

import logging
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from appclass import AutoApp


class Firm_mark_writer():

    answer = None

    def __init__(self, answer):
        self.answer = answer

    def module_mark(self):
        pass



class Firms_marks_writer(Firm_mark_writer):

    def __init__(self):
        pass


