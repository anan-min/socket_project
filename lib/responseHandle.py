from lib.clientThread import *
from exceptions.clientException import client_exit_exception

# helper functions


def handle_response(response, serverAddress):
    """handle response from the server

    Args:
        response (dict): response from the server in term of dict
        serverAddress (list): address and port numebr of server 
    """
    is_client_exit(response)
    if is_file_trasfer_requested(response):
        # what do we need to pass in the thread to process it
        clientThread = ClientThread(response, serverAddress)
        clientThread.start()
    else:
        display_message(response)


def is_file_trasfer_requested(response):
    command = response["command"]
    return command in ["upload file", "download file"]

    # should we encapsulate the implementation here ?


def display_message(response):
    if response:
        print(response["message"])


def is_client_exit(response):
    if response["command"] == "logout":
        raise client_exit_exception
