# -------=======  Imports  =======------- #


# -------======= ◤       ◥ =======------- #
# -------=======    MAIN    =======------- #
# -------======= ◣       ◢ =======------- #

class db_Database():
    def __init__(self, name:str, tabels:list) -> None:

        self.name    =  name
        self.tables  =  tabels
    #  def __init__

    def get_table_names(self):
        
        table_names = []
        for table in self.tables:
            table_names.append( table.name )
        # ⇀

        return table_names
    # def  get_table_names

# class  db_Database()

class db_Table():
    def __init__(self, name:str, columns:list[list], rows:list[list]) -> None:
        
        self.name     =  name
        self.columns  =  columns
        self.rows     =  rows
    # def  __init__

    def get_data(self):

        return (self.name, self.columns, self.rows)
    # def  get_data

# class  db_Table()
