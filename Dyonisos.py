__author__ = 'Maxime'

import threading
from Commandes import Commandes


from appclass import App

Application = App()
Com = Commandes()

def main():

    Com.setapp(Application)

    ThreadProg = threading.Thread(None, Application.run, None)
    ThreadCmd = threading.Thread(None, Com.cmdloop(), None)


    ThreadProg.start()
    #ThreadCmd.start()



if __name__ == '__main__':
    main()