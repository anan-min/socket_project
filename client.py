from fileinput import filename
from socket import *
from bin.utils import *
from bin.clientParse import *
from lib.responseHandle import *
import os
from socket import *
import sys

# Server would be running on the same host as Client
if len(sys.argv) != 3:
    print("\n===== Error usage, python3 TCPClient3.py SERVER_IP SERVER_PORT ======\n")

command_req_str = "Enter one of the following commands: CRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV,XIT: "
serverHost = sys.argv[1]
serverPort = int(sys.argv[2])
serverAddress = (serverHost, serverPort)
clientSocket = socket(AF_INET, SOCK_DGRAM)

# authenticate the user
credential = process_authentication(clientSocket, serverAddress)

while True:
    try:
        input_str = input(command_req_str)
        # create request from the input_str
        request = generate_request(input_str, credential)
        # recieve and convert response to object
        response = udp_communication(request, clientSocket, serverAddress)
        #  handle with the response recived
        handle_response(response, serverAddress)

    except client_exit_exception:
        break
    except command_not_exists:
        print("Invalid command")
    except command_syntax_invalid:
        pass
    except FileNotFoundError:
        print("File not found")

client_exit()
