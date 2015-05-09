__author__ = 'Maxime'

import logging


logging.basicConfig(filename='Data/dyonisos.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='a', level=logging.DEBUG)

from appclass import *




def main():
    Application.run()




if __name__ == '__main__':
    main()