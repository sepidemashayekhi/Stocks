import pyodbc

class Conection:
    def __init__(self):
        self.cnxnStr=("Driver={SQL Server};"
            "Server=DESKTOP-M0SPTTJ;"
            "Database=Stocks;"
            "Trusted_Connection=yes;")
        self.cnxn = pyodbc.connect(self.cnxnStr)
        self.cursor = self.cnxn.cursor()
    
    @property
    def closedConection(self):
        self.cnxn.close()
    