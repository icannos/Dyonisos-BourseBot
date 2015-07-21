__author__ = 'ValadeAurelien'
import Tools.DataMapper
import Tools.loader
import logging

################################## DATAMAPPER ##################################
def init_DataMapper():
    global DataM
    DataM = Tools.DataMapper.DataMapper(database_name='database.db', database_path='data')

def get_DataMapper():
    return DataM

################################## LOGGING ##################################
def init_Logging():
    logging.basicConfig(filename='Data/dyonisos.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='a', level=logging.DEBUG)

################################## LOADER ##################################


#### Depracted
def init_Loader():
    global Loader
    Loader = Tools.loader.Loader()

def get_Loader():
    return Loader

### Config ###
def load_config():
    global config
    config = Loader.load_configuration()

def get_config():
    return config

### Firms ###
def load_firms():
    global firms
    firms = Loader.load_firms()

def get_firms():
    return firms

### Modules ###
def load_modules():
    global modules
    modules = Loader.load_modules()

def get_modules():
    return modules