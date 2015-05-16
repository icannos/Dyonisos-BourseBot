__author__ = 'Maxime'

import logging
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


logging.basicConfig(filename='Data/dyonisos.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='a', level=logging.DEBUG)

from appclass import *




def main():

    AutoApp.run()
    # Everything has to be UPON this function




if __name__ == '__main__':
    main()