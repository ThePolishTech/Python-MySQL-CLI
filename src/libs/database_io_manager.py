# Imports, a classic

from libs.connector_and_cursor import cursor
# -------------------------------------------------------------------------------- #
# ----------------------------------- Def DBio ----------------------------------- #

class Database_IO_Manager(object):
    def __init__(self, db_creds):
        '''Initializes the I/O pathway with provided database credentials'''
        self.db_credentials = db_creds
    # \__init__

    def send_query( self, query:str): # -> ( result||"Success"||err , isErr )
        '''Send MySQL Query\n -> ( result||"Success"||err , isErr )'''
        try:
            with cursor( **self.db_credentials ) as c:
                c.execute( query )
                result = c.fetchall()
        except Exception as Err:
            return ( Err, True )

        if result:
            return ( result, False)
        else:
            return ( '', False)
    # \send_query

# \class
