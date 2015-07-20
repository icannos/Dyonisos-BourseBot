__author__ = 'Atelier'

import GlobalFile
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def after_order(order, lsorders):
    date = order[4]
    for item in lsorders:
        if item[4] < date:
            lsorders.pop()
        else:
            break
    return lsorders

def before_order(order, lsorders):
    date = order[4]
    lsorders.reverse()
    for item in lsorders:
        if item[4] > date:
            lsorders.pop()
        else:
            break
    lsorders.reverse()
    return lsorders

def get_couple_takings(couple):
    takings = 0
    for ope in couple:
        takings += ope[2]
    return takings


class AnalyseModImplicInGivenOrders:

    short, middle, long = None, None, None
    DataM = None
    implications_exe_ord = None
    couples = []
    firms_stories = []
    given_advices = None
    partila_mark = None

    def __init__(self, module_name, short, middle, long):
        self.DataM = GlobalFile.get_DataMapper()
        self.short, self.middle, self.long = short, middle, long
        self.module_name = module_name

    def fetch_implications_in_executed_order(self):
        self.implications_exe_ord = self.DataM.get_all("SELECT * FROM system_executed_order WHERE source = " + self.module_name)

    def get_firm_story_in_given_orders(self, firm_isin):
        story = self.DataM.get_all("SELECT * FROM system_executed_order WHERE ISIN = " + firm_isin)
        return story

    def get_firms_stories_in_given_orders(self):
        implicated_firms = [item[1] for item in self.implications_exe_ord]
        for firm_isin in implicated_firms:
            self.firms_stories.append(self.get_firm_story_in_given_orders(firm_isin))

        # la place des reverse depend de si get_all() renvoie par ordre croissant ou decroissant

    def build_couples(self):
    # building: ([ope(module), ope complementaires(autres modules)]...)
    #ope = (id, firm_isin, +/-money, source, time)

        self.couples = []
        for item in self.implications_exe_ord:
            couple = [item]
            if item[3] > 0:
                for after in self.after_order(item, self.firms_stories):
                    if item[3] * after[3] < 0:
                        couple.append(after)
                    else: #signifie qu'on a rachete une action pour cette entreprise
                        break
            if item[3] < 0:
                for after in self.before_order(item, self.firms_stories):
                    if item[3] * after[3] < 0:
                        couple.append(after)
                    else:
                        break
            self.couples.append(couple)

    def get_module_mark(self,module_name):
        return self.DataM.get_all("SELECT * FROM system_modules_marks WHERE name = " + module_name)

    def analyse_couple(self,couple):
        takings = get_couple_takings(couple)
        """Faire la moyenne des notes de autres modules: valoriser si la recette est positive alors
        que la moyenne est mauvaise, minimiser si la recette est negative et que cette myenne est mauvaise, et
        inversement si la moyenne est bonne"""

    def analyse_couples(self):
        self.partila_mark = sum([couple for couple in self.couples])
        self.partila_mark /= len(self.couples)

    def launch_analyse(self):
        self.fetch_implications_in_executed_order()
        self.get_firms_stories_in_given_orders()
        self.match_infos()
        self.analyse()
        return partial_mark



class AnalyseModImplicThroughGivenAdvices:

    short, middle, long = None, None, None
    DataM = None
    implications_exe_ord = None
    couples = []
    firms_stories = []
    given_advices = None

    def __init__(self, module_name, short, middle, long):
        self.DataM = GlobalFile.get_DataMapper()
        self.short, self.middle, self.long = short, middle, long
        self.module_name = module_name


    def fetch_given_advice(self):
        self.given_advices = self.DataM.get_all("SELECT * FROM system.given_advices WHERE source = " + self.module_name)

    def get_firm_datas(self,firm_isin):
        firm_datas = self.DataM.get_all("SELECT * FROM system.firms_row_figures WHERE isin = " + firm_isin)
        return firm_datas

    def check_advice_validity(self):
        pass





class UpdateModules:

    short, middle, long = None, None, None

    def __init__(self, ):
        config = GlobalFile.get_config()
        self.short, self.middle, self.long = int(config['system.short_range']), int(config['system.middle_range']), int(config['system.long_range'])

