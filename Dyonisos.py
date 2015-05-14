__author__ = 'Maxime'

import logging
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


logging.basicConfig(filename='Data/dyonisos.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='a', level=logging.DEBUG)

from appclass import *




def main():

    Application.run()
    # Tout le code doit se trouver au dessus de cette fonction




if __name__ == '__main__':
    main()