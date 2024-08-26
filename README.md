# ThePolishTech's `Python MySQL CLI` tool
A simple CLI tool for reading MySQL databases. Built as a side-project to test out my own ability as a programmer.
<br>
<br>

## How to install?
Simply clone this repository, then navigate to `\src` and run `main.py` ( this assumes you already have Python v3 installed ). Once it launches you may the commands listed at the bottom of this `README.md`
<br>
<br>

## How did we get here?
Like mentioned above, this tool was made as a side project. Primarily made for fun, it allowed me to test out the logistics of making a CLI tool.
One of the challenges faced was interpreting commands with arguments and error handeling.<br>
For the latter I had adopted a Rust-like pattern based around returning from functions with a tuple, where one value represents whether an error
had occured or not, with the other being either an error
message or the result of the function, depending on the context.<br>
As for the former I used a simple function revolving around spliting the input string whereever whitespace characters occured (' '). However the
lack of support for flags and arguments, as would be found in  `command prompt` / `Linux terminal`  leaves me unsatisfied.
<br>
<br>

## What's next?
While programming this has certainly been fun, my quench for programming goodness has not been brought to an end. My next goal is creating a proper command interpreter,
one which will support flags, arguments, piping, and variables. It will most definitely be written in Rust. This may as well evolve into a custom interpreter
<br>
<br>

## Available Commands
- `quit`
    Quit the Program
  
- `echo`
    Echo text. Must be in `"double quotes"`

- `help`
    Recive help for all available commands

- `lsDB`
    List avalible database configs
  
- `ldDB`
    Connect to DB using config. Use either provided index or use name
  
- `rmDB`
    Remove selected DB. Use either provided index or name
  
- `vwDB`
    View selected config. Use either provided index or name
  
- `mkDB`
    Create DB config
  
- `lsTbl`
    List tables in DB.
  
- `ldTbl`
    Load selected table. Use either provided index or name
  
- `lsRow`
  Present rows in loaded table. Optionally select rows using a single integer or a range denoted by `..`
  
- `rawSq`
  Execute raw SQL on loaded database. Note: tables must be denoted by `database_name.table_name`
