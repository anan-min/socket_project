
from exceptions.clientException import *
import os

'''
command that allowed user to input
'''
valid_commands = ["CRT", "MSG", "DLT", "EDT",
                  "LST", "RDT", "UPD", "DWN", "RMV", "XIT"]



'''
create reqiest from user command, credential, message, and arguments
- store all information on request obj
- request object dicitonary that encoded

parameter
 - command string
 - credential string
 - message string
 - args list of string
'''
def create_request(command, credential, message, args):
    request_dict = {
        'command': command,
        'credential': credential,
        'message': message,
        'args': args
    }
    return str(request_dict).encode()


CRT = "CRT this_is_a_name"
MSG = "MSG this hello my name is nut"
EDT = "thread 1 hello my name is nut"



'''
call by the user to generate reqeust depending on the input_str of the user
parameter:
    input_str: string
    credential: string
output:
    request: encoded string
'''
def generate_request(input_str, credential):
    command = parse_command(input_str)
    args = parse_args(input_str)
    if not valid_command_syntax(command, args):
        print(f"Incorrect syntax for {command}")
        raise command_syntax_invalid
    return create_request(command, credential, None, args)




'''
get command from the input_str
parameter:
    input_str string
raise:
    command_not_exists: command not in valid command
return command string
'''
def parse_command(input_str):
    command = input_str.split(" ")[0]
    if command not in valid_commands:
        raise command_not_exists
    return command


'''
get argument from the input_str depending on the command in the input_str
parameter:
    input_str: string
return args: list(string)
'''
def parse_args(input_str):
    command = input_str.split(" ")[0]
    if command == "MSG":
        return parse_input_with_message(input_str, 3)
    elif command == "EDT":
        return parse_input_with_message(input_str, 4)
    else:
        return parse_input(input_str)


'''
parse input_str depending on the input_size of
parameter:
    input_size: (int) argument size of string
    input_str: (string) user input
return args: list(str)
'''
def parse_input_with_message(input_str, input_size):
    inputs = input_str.split(" ")
    command = inputs.pop(0)

    args = []

    for _ in range(input_size - 2):
        args.append(inputs.pop(0))

    args.append(" ".join(inputs))
    return args


def parse_input(input_str):
    inputs = input_str.split(" ")
    command = inputs.pop(0)
    args = inputs
    return args



'''
check if command and args is in the valid syntax
paramter:
    - command: string
    - args: list(string)
'''
def valid_command_syntax(command, args):
    arg_count = get_args_count(args)
    if command == "CRT" and arg_count == 1:
        return True
    elif command == "MSG" and arg_count == 2:
        return True
    elif command == "DLT" and arg_count == 2 and args[1].isdigit():
        return True
    elif command == "EDT" and arg_count == 3 and args[1].isdigit():
        return True
    elif command == "LST" and arg_count == 0:
        return True
    elif command == "RDT" and arg_count == 1:
        return True
    elif command == "UPD" and arg_count == 2:
        return True
    elif command == "DWN" and arg_count == 2:
        return True
    elif command == "RMV" and arg_count == 1:
        return True
    elif command == "XIT" and arg_count == 0:
        return True

    return False

'''
count args that is not none
parameter
    - args: list(string)
return
    - args_number:
'''
def get_args_count(args):
    return len([arg for arg in args if arg])


