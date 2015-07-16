__author__ = 'Maxime'

from advicegenericscript import advice


class FirmsMarkWriterV2:
    advices = []
    modules_mark = None

    def __init__(self, package=0):
        if package != 0:
            self.advices = self.MakeAdviceList(package)

            for a in self.advices:


    def MakeAdviceList(self, package):
        """
        Transform the package in a one level list
        :rtype :  [advice]
        :param package: It's a list of list, which are coming from the module: [[advice1, advice2, ...], ...]
        """

        for l in inputlist:
            for a in l:
                yield a

    def fetch_modules_mark(self):
        """
        Fetches the marks of all modules and store it in a dic by mod name
        """
        all = self.DataM.get_all("SELECT module_name, markS,markM,markL FROM system_modules_marks")