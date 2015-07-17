__author__ = 'Atelier'

import GlobalFile
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")



class DecisionsWriter():
    """
    Modifies the DB (sys_executed_orders; sys_balance)
    Recieves a ToDoList: ([firm_isin,+/-money,source]...)
    """
    DataM = None
    todolist = None
    newbalance = None
    #todolist ([firm_isin,+/-money,source]...)

    def __init__(self, todolist):
        """
        Initialization, returns nothing
        """
        self.DataM = GlobalFile.get_DataMapper()
        self.todolist = todolist
        #todolist ([firm_isin,+/-money,source]...)

    def fetch_old_balance(self):
        """
        Fetches the old balance by reading the DB. Returns nothing.
        """
        (self.oldbalance) = self.DataM.get_one('SELECT balance FROM system_balance ORDER BY time DESC LIMIT 1')

    def calculate_new_balance(self):
        """
        Calculates the new balance thanks to de todolist. Returns nothing.
        """
        self.fetch_old_balance()
        self.newbalance = sum([item[1] for item in self.todolist]) + self.oldbalance

    def modify_balance(self):
        """
        Writes the new balance in the DB sys_balance. Returns nothing.
        """
        self.calculate_new_balance()
        self.DataM.execute('INSERT INTO system_balance VALUES (?, ?, ?)', (None, self.newbalance, time.time()))

    def arrange_todolist(self):
        """
        Modifies the todolist so that it can be inserted in the DB sys_executed_orders. Returns nothing
        """
        Modif = [[None]+item+[time.time()] for item in self.todolist]
        self.todolist = Modif

    def update_executed_orders(self):
        """
        Updates the DB sys_executed_orders by inserting new lines. Returns nothing.
        """
        self.arrange_todolist()
        self.DataM.executemany('INSERT INTO system_executed_orders VALUES (?, ?, ?, ?, ?, ?)', self.todolist)

    def write_decisions(self):
        """
        Modifies the DB sys_balance & sys_executed_orders by inserting new lines in each one.
        """
        self.modify_balance()
        self.update_executed_orders()