__author__ = 'Atelier'

import GlobalFile
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class UpdateModule():

    short, middle, long = None, None, None
    DataM = None
    implications_exe_ord = None
    firms_stories = []
    couples = []

    def __init__(self, module_name):
        self.DataM = GlobalFile.get_DataMapper()
        self.module_name = module_name

    def fetch_implications_in_executed_order(self):
        self.implications_exe_ord = self.DataM.get_all("SELECT * FROM system_executed_order WHERE source = " + self.module_name)

    def get_firm_story(self, firm_isin):
        self.firms_stories.append(self.DataM.get_all("SELECT * FROM system_executed_order WHERE ISIN = " + firm_isin))

    def get_firms_stories(self):
        implicated_firms = [item[1] for item in self.implications_exe_ord]
        for firm_isin in implicated_firms:
            self.get_firm_story(firm_isin)


        # la place des reverse depend de si getall() renvoie par ordre croissant ou decroissant

    def after_order(self, order, lsorders):
        date = order[4]
        for item in lsorders:
            if item[4] < date:
                lsorders.pop()
            else:
                break
        return lsorders

    def before_order(self, order, lsorders):
        date = order[4]
        lsorders.reverse()
        for item in lsorders:
            if item[4] > date:
                lsorders.pop()
            else:
                break
        lsorders.reverse()
        return lsorders


    def match_infos(self):
    # building: ([ope(module), ope complementaires(autres modules)]...)
        self.couples = []
        for item in self.implications_exe_ord:
            couple = [item]
            if item[3] > 0:
                for after in self.after_order(item, self.firms_stories):
                    if item[3] * after[3] < 0:
                        couple.append(after)
                    if abs(after[3]) >= abs(item[3]):
                        break
            if item[3] < 0:
                for after in self.before_order(item, self.firms_stories):
                    if item[3] * after[3] < 0:
                        couple.append(after)
                    if abs(after[3]) >= abs(item[3]):
                        break
            self.couples.append(couple)





class UpdateModules():

    short, middle, long = None, None, None

    def __init__(self, ):
        config = GlobalFile.get_config()
        self.short, self.middle, self.long = int(config['system.short_range']), int(config['system.middle_range']), int(config['system.long_range'])

