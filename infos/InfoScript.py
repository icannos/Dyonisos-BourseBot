__author__ = 'Maxime'


class InfoScript:

    scriptname = 'Infoscript'


    conf = []

    def __init__(self, conf):
        self.setconf(conf)

    def setconf(self, conf):
        self.conf = conf

    def run(self):
        self.conf = self.conf

