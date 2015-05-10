__author__ = 'Maxime'

from loader import Loader
import logging
import time

class App:

    data = []
    conf = {}
    modules = []
    modulesInstances = {}
    on = 1

    def __init__(self):
        logging.info("================= Dyonisos ======================")
        logging.info("================= Initialisation ================")
        loader = Loader()
        logging.info("================= Chargement des parametres ================")
        self.conf = loader.loadconfiguration()

        logging.info("================= Chargement des modules ================")
        self.modules = loader.loadmodules()

        logging.info("================= Instanciation des modules ================")

        for m in self.modules:
            mod = getattr(m[2], m[1])

            if not m[0] in self.modulesInstances.keys():
                self.modulesInstances[m[0]] = {}

            self.modulesInstances[m[0]][m[1]] = mod(self.conf)
            logging.info(m[0] + '.' + m[1] + ' Init Ok')

    def stop(self):
        self.on = 0

    def run_infos(self):
        for m in self.modules:
            if m[0] == 'infos':
                instance = self.modulesInstances['infos'][m[1]]
                instance.setconf(self.conf)
                instance.run()

    def run_decision(self):
        for m in self.modules:
            if m[0] == 'decision':
                instance = self.modulesInstances['decision'][m[1]]
                instance.setconf(self.conf)
                instance.run()

    def run_analyse(self):
        """

        :rtype : Void
        """
        for m in self.modules:
            if m[0] == 'analyse':
                instance = self.modulesInstances['analyse'][m[1]]
                instance.setconf(self.conf)
                instance.run()

    def run(self):
        logging.info("================= Lancement =====================")
        while self.on:
            self.run_infos()

            self.run_analyse()

            self.run_decision()

            # Valeur issue de la configuration "system_configuration" de la db
            time.sleep(self.conf['system.sleeptime'])

        logging.info("Arret")


global Application
Application = App()