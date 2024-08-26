# -------=======  Imports  =======------- #
import yaml
    # Libs
from libs.db_classes import db_Database, db_Table
from libs.database_io_manager import Database_IO_Manager


# -------======= ◤       ◥ =======------- #
# -------=======    MAIN    =======------- #
# -------======= ◣       ◢ =======------- #

class db_loader(object):
    def __init__(self) -> None:
        pass
    # __init___

    def get_default_db_credentials(CONFIG_PATH_in) -> dict:
        '''Returns the default DB's credentials'''

        with open( f"{CONFIG_PATH_in}\\default_db_credentails.yaml", "r" ) as yaml_in:

            config = yaml.safe_load(yaml_in)
            db_credentials = {                            # setting the credentials from database_credentials
            'host': config["DATABASE"]["HOST"],
            'database': config["DATABASE"]["DB"],
            'user': config["DATABASE"]["USERNAME"],
            'password': config["DATABASE"]["PASSWORD"],
            'charset': config["DATABASE"]["CHARSET"]
        }
        return db_credentials
    # get_default_db_credentials

    def read_db_credentials(PATH_TO_CONFIG_in, file_name):
        '''Read DB credentials from file\n **file_name includes extension**'''
        
        try:
            with open(  f"{PATH_TO_CONFIG_in}\\{file_name}", 'r'  ) as yaml_in:
                data = yaml.safe_load(yaml_in)
                db_credentials = {
                    'host': data["DATABASE"]["HOST"],
                    'database': data["DATABASE"]["DB"],
                    'user': data["DATABASE"]["USERNAME"],
                    'password': data["DATABASE"]["PASSWORD"],
                    'charset': data["DATABASE"]["CHARSET"]
                }
        except Exception as Err:
            return ( Err, True )
        return ( db_credentials, False )
    # read_db_credentials

    def load_db(DB_CREDS_in):
        '''Loads given DB into a \'db_Database\' class -> ( \'db_Database\' || err, isErr )'''
        load_db_io_manager = Database_IO_Manager(DB_CREDS_in) 

        # Returns with an error if the query malfunctions
        cache = load_db_io_manager.send_query(f"SHOW TABLES FROM {DB_CREDS_in['database']};") # QUERY RESULT: Reutrns a list containing the names of tables in DB
        result = cache[0]
        if cache[1]:
            return ( result, True )
            
        # Populates 'table_names' with the names of the tables in database
        table_names = []
        for table_name in result:
            table_names.append( table_name[0] )
        
        # Creates list 'tables' then populates with 'db_Table' objects
        tables = []
        for table_name in table_names:
            # Per Column Flags
            cache = load_db_io_manager.send_query(f"SHOW COLUMNS FROM {table_name};")
            result = cache[0]
            
            column_metadata = []
            for column_a in result:
                column_metadata.append( column_a )
            
            # Fill in the Rows
            cache = load_db_io_manager.send_query(f"SELECT * FROM {table_name};")
            result = cache[0]

            rows = []
            for row in result:
                rows.append(row)
                
            tables.append(  db_Table(table_name, column_metadata, rows)  )

        # Pack everything into 'database' and return it
        database = db_Database(  DB_CREDS_in["database"], tables  )
        return ( database, False)
    # load_db

# db_loader()