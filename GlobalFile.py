__author__ = 'ValadeAurelien'
import Tools.DataMapper
import logging


def init_DataMapper():
    global DataM
    DataM = Tools.DataMapper.DataMapper(database_name='database.db', database_path='data')


def get_DataMapper():
    return DataM


def init_Logging():
    logging.basicConfig(filename='Data/dyonisos.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='a', level=logging.DEBUG)

