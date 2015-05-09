__author__ = 'Maxime'

from loader import Loader
import logging


class App:

    data = []
    conf = []
    modules = []
    modulesinstances = {}
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

            if not m[0] in self.modulesinstances.keys():
                self.modulesinstances[m[0]] = {}

            self.modulesinstances[m[0]][m[1]] = mod(self.conf)
            logging.info(m[0] + '.' + m[1] + ' Init Ok')

    def stop(self):
        self.on = 0

    def run_infos(self):
        for m in self.modules:
            if m[0] == 'infos':
                instance = self.modulesinstances['infos'][m[1]]
                instance.setconf(self.conf)
                instance.run()

    def run_decision(self):
        for m in self.modules:
            if m[0] == 'decision':
                instance = self.modulesinstances['decision'][m[1]]
                instance.setconf(self.conf)
                instance.run()

    def run_decision(self):
        for m in self.modules:
            if m[0] == 'decision':
                instance = self.modulesinstances['decision'][m[1]]
                instance.setconf(self.conf)
                instance.run()

    def run_analyse(self):
        for m in self.modules:
            if m[0] == 'analyse':
                instance = self.modulesinstances['analyse'][m[1]]
                instance.setconf(self.conf)
                instance.run()

    def run(self):
        logging.info("================= Lancement =====================")
        while self.on:
            self.run_infos()

            self.run_analyse()

            self.run_decision()

        logging.info("Arret")


global Application
Application = App()