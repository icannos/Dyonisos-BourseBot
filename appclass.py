__author__ = 'Maxime'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


from loader import Loader
import logging
import time
import Tools.DataMapper as DM
import Mark_maker

class App:

    data = []
    conf = {}
    modules = []
    modulesInstances = {}
    on = 1

    DataM = None

    def __init__(self):
        logging.info("================= Dyonisos ======================")

        logging.info("================= DataMapper ======================")
        self.DataM = DM.DataMapper(database_name='database.db', database_path='data')

        logging.info("================= Initialisation ================")
        loader = Loader(self.DataM)
        logging.info("================= Loading settings ================")
        self.conf = loader.load_configuration()

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
                    yield (instance.answer)
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
                    yield (instance.answer)
                except SystemError as error:
                    logging.warning(error[0])

    def run_marks_maker(self, generator):
        for answer in generator:
                Mark_maker.Mark_maker(answer)

    def run(self):
        logging.info("================= Lancement =====================")
        while self.on:
            gath_gene = self.run_gatherer()
            math_gene = self.run_mathsanalysis()

            self.run_marks_maker(gath_gene)
            self.run_marks_maker(math_gene)

            # Futur place of Module Markupdate

            # Value found in the "system_configuration" table
            time.sleep(float(self.conf['system.sleeptime']))

        logging.info("Arret")
        return 0


global AutoApp
AutoApp = App()