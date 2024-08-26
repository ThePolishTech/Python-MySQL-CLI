# -------=======  Imports  =======------- #
import os
import yaml
    # Bespoke Libs
from libs.db_loader import db_loader

# -------======= ◤       ◥ =======------- #
# -------=======    MAIN    =======------- #
# -------======= ◣       ◢ =======------- #

def get_program_root_path() -> str:
        '''Returns the pre-determened path of the program\n
        ( Relative to \"src/sub/utils.py\" )'''
        current_path = os.path.abspath(__file__)
        for i in range(3):
            current_path = os.path.dirname(current_path)
        return current_path
    # get_program_root_path()

def validate_DB_configs(DB_CREDENTIALS_PATH_in: str) -> tuple[list, bool]:
    '''Verify intergrity of config \'.yaml\'s and return list of valid configs + flag if any are invalid'''
    DB_loader = db_loader
    dir_contents = os.listdir(DB_CREDENTIALS_PATH_in)

    valid_configs = []
    isErr = False
    for config in dir_contents:
        cache = DB_loader.read_db_credentials(DB_CREDENTIALS_PATH_in, config)
        if cache[1]:
              isErr = True
        else:
            valid_configs.append( config )
    # ⇀
    return ( valid_configs, isErr )

def create_DB_config(DB_CREDENTIALS_PATH_in: str, db_credentials: dict) -> tuple[str, bool]:
    '''Create DB config from inputed dict'''

    try:
        credentials_name = db_credentials['DATABASE']["DB"]
        with open( f"{DB_CREDENTIALS_PATH_in}\\{credentials_name}.yaml", 'w' ) as file_out:
            yaml.safe_dump(db_credentials, file_out)
        return ["", False]
    except Exception as Err:
        return [Err, True]

def split_cmd_and_argument(string_in: str) -> tuple[str, str, str]:
    '''Split the input into command, first argument, all arguments'''

    command    = string_in.split(" ")[0]
    argument   = string_in.removeprefix(f"{command}")[1:]
    arguments  = string_in[len(command)+1:]

    return (command, argument, arguments)

def select_rows_from_argument(argument_in: str, rows_in: list) -> tuple[list, bool]:
    '''Using a regular index or a range, return the rows using them\nCAUTION: Use one-based indexing, this is to match with DB row indexing\nNOTE: Go to definition for notes about functionality'''
    # NOTES:
    #    ↳ As previously mentioned, this function uses one-based indexing to fit in with DB table scheme
    #    ↳ If no arguments are provided, Return the entire 'rows_in' variable
    #    ↳ Range is **INCLUSIVE** on both numbers, over-bounds indexes will result in all indexes above the first being included

    argument_in = argument_in.strip() # Remove trailing spaces

    # --== EDGE CASES ==-- #

    # If no Arguments, Return early
    if argument_in == "":
        return ( rows_in, False ) # NoErr
    

    # If 'arguments_in' is just an index, return that index
    if argument_in.isdigit():
        if int(argument_in) > len( rows_in ):
            return ( "ERROR: Requested index out of bounds", True )
        return ( rows_in[ (int(argument_in)) -1 ], False ) # NoErr, +Remember: One-Based Indexing
    

    # --== Compute and Select Range ==-- #
    #    ↳ Logically, the only possibilities are: Range Selection or Invalid Input
    first_num = ""
    secnd_num = ""
    seperator = ""
    isFirst_num = True

    for char in argument_in:

        if char.isdigit():
            # Its a digit, put it in the right box

            if isFirst_num:
                first_num += char
            else:
                secnd_num += char
            # ⇀
        else:
            # Its a non-digit, remember it, ONLY if 'isFirst_num == False'
            isFirst_num = False
            seperator += char
        # ⇀
    # ⇀

    if not seperator == "..":    # Make sure syntax is valid, else Err
        return ( f"ERROR: Invalid Range Syntax: '{seperator}'", True ) # IsErr

    first_num = int(first_num) -1 # One-Based indexing
    secnd_num = int(secnd_num) 
    rows_out  = rows_in[first_num:secnd_num]

    return ( rows_out, False ) # NoErr
