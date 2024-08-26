# -------=======  Imports  =======------- #
    # Non Bespoke
import os
import time
    # Bespoke Libs
from libs.database_io_manager import Database_IO_Manager
from libs.db_loader import db_loader

from libs.utils import get_program_root_path
from libs.utils import validate_DB_configs
from libs.utils import split_cmd_and_argument
from libs.utils import select_rows_from_argument
from libs.utils import create_DB_config

# -------=======  Constant Variables  =======------- #
ROOT_PROGRAM_PATH = get_program_root_path()
'''The root path of the program'''
CONFIG_PATH = os.path.join(ROOT_PROGRAM_PATH, "config")
'''The config path of the program'''
DB_CREDENTIALS_PATH = os.path.join(CONFIG_PATH, "db_credentials")
'''The credentials path of the program'''
DEFAULT_DB_CREDS = db_loader.get_default_db_credentials(CONFIG_PATH)
'''Dict( host, database, user, password, charset )'''

# -------=======  Function Definitions  =======------- #
def clear_screen():
    '''Clears the screen and produces a splash'''
    os.system('cls')
    lines = [
        "Type 'help' for information about available commands",
        "  and 'quit' to exit                   - Made by TPT",
        "                                                    ",
        "    ----====  Python SQL CLI  ====----              ",
        "        enter command below to run                  "
    ]
    
    for line in lines:
        print( line )

    print(f"{'-'*120}\n")

# -------=======  Class Definitions  =======------- #
db_io_manager = Database_IO_Manager(DEFAULT_DB_CREDS)
'''I/O pathway for interfacing with databases'''


# -------======= ◤       ◥ =======------- #
# -------=======    MAIN    =======------- #
# -------======= ◣       ◢ =======------- #


# Variable Definitions
db_name      = ""
tbl_name     = ""

loaded_DB        = None
loaded_DB_creds  = None
cached_DBs       = None
selected_DB      = None

loaded_Tbl       = None
cached_tbls      = []
selected_tbl     = None

loaded_Rows      = []

valid_configs, areInvalid_configs = validate_DB_configs(DB_CREDENTIALS_PATH)
cached_DBs = [cfg.removesuffix(".yaml") for cfg in valid_configs]

# Help dict for commands
command_help: dict = {
     "quit": "Quit the Program",
     "lsDB": "List avalible database config",
     "ldDB": "Connect to DB using config",
     "rmDB": "Remove selected DB",
     "vwDB": "View selected config",
     "mkDB": "Create DB config",
    "lsTbl": "List tables in DB",
    "ldTbl": "Load selected table",
    "lsRow": "Show rows in table",
    "rawSq": "Execute raw SQL",
     "echo": "print input"
}




clear_screen()
print()
# Main Loop
while True:
    # Preface
    print(f"{'='*120}")
    if not tbl_name == "":
        working_dir  =  f"{db_name}/{tbl_name}"
    else:
        working_dir  =  f"{db_name}"
    command_in_raw = input(f"{working_dir}/> ")
    command_in, argument_in, arguments_in = split_cmd_and_argument(command_in_raw)
    


    # --== Command Tree to Follow ==-- #

    # Allow user to quit in a more... Fluid way
    if command_in_raw == "quit":
        clear_screen()
        print(f"\n{'='*120}")
        print(f"{working_dir}/> quiting", end="")


        for i in range(3):
            time.sleep(0.1120)
            print(".", end="")
        # ⇀
        break
    # ⇀




    elif command_in == "lsDB":
        clear_screen()
        valid_configs, areInvalid_configs = validate_DB_configs(DB_CREDENTIALS_PATH)
        cached_DBs = [cfg.removesuffix(".yaml") for cfg in valid_configs]
        
        if areInvalid_configs:
            print(f"Saved Databases:  CAUTION: Some saved configs failed to validate")
        else:
            print(f"Saved Databases:")

        for index, cfg in enumerate(cached_DBs):
            print(f"\t{index}  {cfg}")
    # ⇀
    
    elif command_in == "ldDB":
        clear_screen()
        selector = argument_in

        try: # Really wish i could use a Rust Match statement here instead of Try/Except
            selector = int(selector)
            if selector >= len(cached_DBs):
                print("ALERT: Selected index is too large")
                continue
            else:
                selected_DB = cached_DBs[selector]
            # ⇀

        except:
            if selector in cached_DBs:
                selected_DB = selector
            else:
                print("ALERT: Selected DB does not exsist")
                continue
            # ⇀
        
        print(f"Loading DB: {selected_DB}")
        print(f"{'='*120}\n{working_dir}/> ", end="") # Makes the possible wait time look nice


        result, isErr = db_loader.read_db_credentials(DB_CREDENTIALS_PATH, f"{selected_DB}.yaml")
        if isErr:
            print(f"ERROR: {result}")
            continue
        # ⇀
        loaded_DB_creds = result
        result, isErr = db_loader.load_db(result)
        clear_screen()
        if isErr:
            print(f"ERROR: {result}")
            continue
        else:
            loaded_DB  = result
            loaded_Tbl = None
        # ⇀

        cached_tbls = []
        for tbl in loaded_DB.tables:
            cached_tbls.append(tbl.name)

        print("DB loaded")
        db_name = loaded_DB.name
    # ⇀

    elif command_in == "lsTbl":
        clear_screen()
        if cached_tbls == []:
            print("ALERT: No DB loaded")
            continue

        print(f"{loaded_DB.name}/tables")
        for index, table in enumerate(cached_tbls):
            print(f"  {index}: {table}")
    # ⇀

    elif command_in == "ldTbl":
        clear_screen()

        if loaded_DB == None:
            print("ALERT: No DB loaded")
            continue
        
        try:
            argument_in = int(argument_in)
            if argument_in >= len(cached_tbls):
                print("ALERT: Index out of range")
                continue
            tbl_name = cached_tbls[argument_in]
        
        except:
            if not argument_in in cached_tbls:
                print(f"ALERT: Table '{argument_in}' does not exsist\n  Please slelect one of the following: {cached_tbls}")
                continue
            tbl_name = argument_in

        for tbl in loaded_DB.tables:
            if tbl.name == tbl_name:
                loaded_Tbl = tbl
                break
        print(f"Loaded Table: {tbl_name}")
    # ⇀

    elif command_in == "lsRow":
        if loaded_Tbl == None:
            clear_screen()
            print("ERROR: No Table Loaded")
            continue

        # -= LOAD ROWS =- #
        loaded_Rows = []
        for row in loaded_Tbl.rows:
            loaded_Rows.append(row)
        # ⇀
        
        # -= GET ROWS =- #
        clear_screen()
        result, isErr = select_rows_from_argument(argument_in, loaded_Rows)
        if isErr:
            print(result)
            continue
        # ⇀
        
        # -= CREATE OUTPUT BUFFER =- #
        output_buffer = []
        cache = []
        for column_data in loaded_Tbl.columns:
            cache.append(column_data[0])    # Append Column Names
        # ⇀
        output_buffer.append(cache)
    
        if type(result) == tuple:
            output_buffer.append(list(result))
        else:
            for row in result:
                output_buffer.append(list(row))
        # ⇀

        # -= CALCULATE MAX LENGTH =- #
        target_cell_len = [0]*len(output_buffer[0])
        
        for row in output_buffer:
            for cell_index, cell in enumerate(row):
                if len(str(cell)) > target_cell_len[cell_index]:
                    target_cell_len[cell_index] = len(str(cell))
            # ⇀  ⇀
        # ⇀

        # -= PRINT RESULT =- #
        for row_index, row in enumerate(output_buffer):
            
            if row_index == 1:                   # Add a line of seperators
                cache  = sum(target_cell_len) 
                cache += 3*len(target_cell_len)
                cache += 1

                print('-'*cache)

            print(end="| ")
            for cell_index, cell in enumerate(row):
                cache = target_cell_len[cell_index] - len(str(cell))
                print(f"{cell}{' '*cache} | ", end="")
            print()
        # ⇀
    # ⇀

    elif command_in == "mkDB":
        clear_screen()
        print(f"\n{'='*120}")

        fields_to_assign = ['CHARSET', 'HOST', 'DB', 'PASSWORD', 'USERNAME']
        assigned_fields = {}
        fields_len = len(fields_to_assign)

        for _ in range(fields_len):
            field = fields_to_assign[-1]


            field_data_in = input( f"{field}: " )
            assigned_fields.update( {field: field_data_in} )
            fields_to_assign.pop()

        cache = create_DB_config(DB_CREDENTIALS_PATH, {'DATABASE': assigned_fields})
        result = cache[0]

        clear_screen()
        if cache[1]:
            print(f"ERROR: {result}")
        else:
            print("Config Created")
    # ⇀

    elif command_in == "rmDB":
        clear_screen()
        selector = argument_in

        try:
            selector = int(selector)
            if selector >= len(cached_DBs):
                print("ALERT: Selected index is too large")
                continue
            else:
                selected_DB = cached_DBs[selector]
            # ⇀

        except:
            if selector in cached_DBs:
                selected_DB = selector
            else:
                print("ALERT: Selected DB does not exsist")
                continue
            # ⇀
        
        print(f"CONFIRM: Remove DB '{selected_DB}'?    Type 'YES' To Confirm")
        confirmation = str(input( f"{'='*120}\n{working_dir}/> " ))

        if not confirmation == "YES":
            clear_screen()
            print("Aborting DB Config Deletion")
            continue
        else:
            clear_screen()
            print("Deleating")
            os.remove(f"{DB_CREDENTIALS_PATH}\\{selected_DB}.yaml")
            clear_screen()
            print("Config Deleted")
    # ⇀

    elif command_in == "vwDB":
        clear_screen()
        selector = argument_in

        try:
            selector = int(selector)
            if selector >= len(cached_DBs):
                print("ALERT: Selected index is too large")
                continue
            else:
                selected_DB = cached_DBs[selector]
            # ⇀

        except:
            if selector in cached_DBs:
                selected_DB = selector
            else:
                print("ALERT: Selected DB does not exsist")
                continue
            # ⇀
        
        result, isErr = db_loader.read_db_credentials(DB_CREDENTIALS_PATH, f"{selected_DB}.yaml")
        if isErr:
            print(f"ERROR: {result}")
            continue

        print("CONTENTS:\n")
        for field in result:
            whitespace_len = 10 - len(field)
            print(end= f"{' '*whitespace_len}")
            print(f"{field.upper()}: {result[field]}")




    elif command_in == "rawSq":

        # Edge Case
        if loaded_DB_creds == None:
            clear_screen()
            print("ERROR: No Database Loaded")
            continue

        clear_screen()
        result, isErr = db_io_manager.send_query(argument_in)
        if isErr:
            print(f"ERROR: {result}")
        else:
            if result:
                print(f"SUCCESS: {result}")
            else:
                print(f"SUCCESS")
        
        # Reload DB
        result, isErr = db_loader.load_db(loaded_DB_creds)
        if isErr:
            clear_screen()
            print(f"ERROR: {result}")
            continue
        else:
            loaded_DB  = result

        for tbl in loaded_DB.tables:
            if tbl.name == tbl_name:
                loaded_Tbl = tbl
                break
    # ⇀

    elif command_in == "help":
        clear_screen()

        if argument_in == "":
            print("Showing list of commands: ")
            for index, command in enumerate(command_help):

                whitespace_len = 7 - len(command)
                print(  f"{' '*whitespace_len}{command}: -- {command_help[command]}"  )
            continue
        else:
            if argument_in in command_help:
                print(f"{argument_in}: {command_help[argument_in]}")
            else:
                print(f"ALERT: Command '{argument_in}' not recognized")
    # ⇀

    elif command_in == "echo":
        clear_screen()
        if argument_in == "":
            print("ALERT: Argument is Empty")
            continue

        isIn_quotes = False
        output = ""
        for char in arguments_in:

            if char == "\"":
                isIn_quotes = not isIn_quotes
                continue
            
            if isIn_quotes == True:
                output += char

        print(output)
    # ⇀

    # Catchall statement
    else:
        clear_screen()
        if command_in == "":
            print()
            continue
        print(f"ALERT: '{command_in}' command doesn't exsist")
    # ⇀

