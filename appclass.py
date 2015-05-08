__author__ = 'Maxime'

from loader import Loader


class App:

    data = []
    conf = []
    modules = []
    modulesinstances = {}
    on = 1

    def __init__(self):
        print("================= Dyonisos ======================")
        print("================= Initialisation ================")
        loader = Loader()
        print("================= Chargement des parametres ================")
        self.conf = loader.loadconfiguration()

        print("================= Chargement des modules ================")
        self.modules = loader.loadmodules()

        print("================= Instanciation des modules ================")

        for m in self.modules:
            mod = getattr(m[2], m[1])

            if not m[0] in self.modulesinstances.keys():
                self.modulesinstances[m[0]] = {}

            self.modulesinstances[m[0]][m[1]] = mod(self.conf)
            print(m[0] + '.' + m[1] + ' Init Ok')

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
        print("================= Lancement =====================")
        while self.on:
            self.run_infos()

            self.run_analyse()

            self.run_decision()

        print "Arret"
