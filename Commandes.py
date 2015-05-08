__author__ = 'Maxime'

import cmd


class Commandes(cmd.Cmd):

    def setapp(self, app):
        self.app = app

    def do_stop(self, line):
        self.app.stop()
        return True
