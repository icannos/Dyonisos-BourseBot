__author__ = 'Maxime'

from AppClass import App
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def main():
    autoapp = App()
    autoapp.run()
    # Everything has to be UPON this function

if __name__ == '__main__':
    main()