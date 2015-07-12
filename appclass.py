__author__ = 'Maxime'

import GlobalFile
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from Tools.loader import Loader
import time
import Google_parse.GoogleParse as Gp
import Mark_maker.FirmsMarksWriter as MmF
import logging



class App():

    data = []
    conf = {}
    firms = []

    modules = []
    modulesInstances = {}
    on = 1

    google = None
    DataM = None

    def __init__(self):
        GlobalFile.init_Logging()
        logging.info("================= Dyonisos ======================")
        logging.info("================= DataMapper ======================")
        GlobalFile.init_DataMapper()
        self.DataM = GlobalFile.get_DataMapper()
        logging.info("================= Initialisation ================")
        loader = Loader(self.DataM)
        logging.info("================= Loading settings ================")
        self.conf = loader.load_configuration()
        logging.info("================= Loading GoogleParse ================")
        self.google = Gp.GoogleParse()
        logging.info("================= Loading Firms ================")
        self.firms = loader.load_firms()
        logging.info("================= Loading modules ================")
        self.modules = loader.load_modules()
        logging.info("================= Instantiation ================")
        for m in self.modules:
            # Get the class object of the module
            mod = getattr(m[2], m[1])

            # Declare dictionary in each cells of the list to make en 2*2 dictionary
            if not m[0] in self.modulesInstances.keys():
                self.modulesInstances[m[0]] = {}

            # Instantiation of the module with self.conf as init argument
            self.modulesInstances[m[0]][m[1]] = mod(self.conf)
            logging.info(m[0] + '.' + m[1] + ' Init Ok')

    def stop(self):
        self.on = 0

    def run_gatherer(self):
        """
        Launch the pick up tool of the application, to get some data from the web
        """
        for m in self.modules:
            if m[0] == 'Gatherer':
                instance = self.modulesInstances['Gatherer'][m[1]]
                #Reset Conf in doubt of a change
                instance.setconf(self.conf)
                try:
                    instance.run()
                    yield (instance)
                except SystemError as error:
                    logging.warning(error[0])

    def run_maths_analysis(self):
        """
        Launch the mathematical analysis on the data which are already saved on our database
        """
        for m in self.modules:
            if m[0] == 'Maths_analysis':
                instance = self.modulesInstances['Maths_analysis'][m[1]]
                #Reset Conf in doubt of a change
                instance.setconf(self.conf)
                try:
                    instance.run()
                    yield (instance)
                except SystemError as error:
                    logging.warning(error[0])

    def run_firms_marks_maker(self, g_modules_packages):
        MmF.FirmsMarksWriter(g_modules_packages)

    def run(self):
        logging.info("================= Lancement =====================")
        while self.on:
            self.google.save_firms_data(self.firms)

            gath_gene = self.run_gatherer()
            math_gene = self.run_maths_analysis()
            self.run_firms_marks_maker(gath_gene)
            self.run_firms_marks_maker(math_gene)
            # Future place of Module MarkUpdate

            # Value found in the "system_configuration" table
            float(self.conf['system.sleeptime'])
            logging.info("Again a run")

        logging.info("Exit")
        return 0
