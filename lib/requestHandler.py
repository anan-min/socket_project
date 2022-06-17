# get a request object
# return message to the client
from exceptions.threadException import *
from exceptions.fileException import *
from lib.auth import *
from bin.response import *
from socket import *
import os
authentication_commands = ["username_check", "password_check", "XIT"]
file_transfer_commands = ["UPD", "DWN"]


def send_response(serverSocket, clientAddress, response):
    serverSocket.sendto(response, clientAddress)


def requestHandler(request_encode, serverSocket,  tcpServerSocket,  clientAddress, serverAddress, data):
    """handle with encoded request

    Args:
        request_encode (encoded str): request from the server
        serverSocket (list): udp socket
        tcpServerSocket (socket): tcp socket
        clientAddress (list): address and port number of client
        serverAddress (_type_): address and port number of server
        data (Forum_data): data for forum and authentication
    """
    auth_data = data.auth_data
    forum = data.forum

    request = eval(request_encode.decode())
    command = request["command"]

    if command in authentication_commands:
        response = auth_handler(request, clientAddress, auth_data)
        send_response(serverSocket, clientAddress, response)
    elif command in file_transfer_commands:
        file_transfer_handler(serverSocket, tcpServerSocket, serverAddress,
                              clientAddress, request, forum)
    else:
        response = command_handler(request, forum)
        send_response(serverSocket, clientAddress, response)


def auth_handler(request, clientAddress, auth_data):
    """ handle response realated to authentication

    Args:
        request (dict): request that need to be handle
        clientAddress (list): address and port number of client
        auth_data (AuthData): data related to the authenication

    Returns:
        response: response about authentication
    """
    response = None
    if request["command"] == "username_check":
        response = username_check(request, clientAddress, auth_data)
    elif request["command"] == "password_check":
        response = password_check(request, clientAddress, auth_data)
    elif request["command"] == "XIT":
        response = logout_user(request, clientAddress, auth_data)
    return response


def command_handler(request, forum):
    """handle command that is not related to authentication

    Args:
        request (dict): request content in form of dict
        forum (ForumThreads): object that store forum information

    Returns:
        response: response to the command requested
    """
    command, args, username = request_parse(request)
    if command == "CRT":
        return crt_handler(args, username, forum)
    elif command == "MSG":
        return msg_handler(args, username, forum)
    elif command == "DLT":
        return dlt_handler(args, username, forum)
    elif command == "EDT":
        return edt_handler(args, username, forum)
    elif command == "LST":
        return lst_handler(username, forum)
    elif command == "RDT":
        return rdt_handler(args, username, forum)
    elif command == "RMV":
        return rmv_handler(args, username, forum)


def file_transfer_handler(serverSocket, tcpServerSocket, serverAddress, clientAddress, request, forum):
    """handle file tra

    Args:
        serverSocket (socket): udp socket of server
        tcpServerSocket (socket): tcp socket of server
        serverAddress (list): addrress and port number of server
        clientAddress (list): address and port numebr of client
        request (dict): request from the client
        forum (ForumThreads): object that store data about forum
    """
    command, args, username = request_parse(request)
    if command == "UPD":
        upd_handler(serverSocket, tcpServerSocket, serverAddress,
                    clientAddress, args, username, forum)
    elif command == "DWN":
        dwn_handler(serverSocket, tcpServerSocket, serverAddress,
                    clientAddress, args, username, forum)


def crt_handler(args, username, forum):
    """handle create thread  command
    Args:
        args (list): argument for command
        username (str): client username
        forum (ForumThread): objec that store all forum data
    Returns:
        response(encoded str): response on creating thread
    """
    thread_title = args[0]
    user_issue_command(username, "CRT")
    return forum.create_thread(thread_title,  username)


def msg_handler(args, username, forum):
    """handle post message command command
    Args:
        args (list): argument for command
        username (str): client username
        forum (ForumThread): objec that store all forum data
    Returns:
        response(encoded str): response on post message command
    """
    thread_title, message = args[0], args[1]
    user_issue_command(username, "MSG")
    return forum.post_message(thread_title, message, username)


def dlt_handler(args, username, forum):
    """handle delete message command
    Args:
        args (list): argument for command
        username (str): client username
        forum (ForumThread): objec that store all forum data
    Returns:
        response(encoded str): response on delete message command
    """
    thread_title, message_number = args[0], int(args[1])
    user_issue_command(username, "DLT")
    return forum.delete_message(thread_title, message_number, username)


def edt_handler(args, username, forum):
    """handle edit message command
    Args:
        args (list): argument for command
        username (str): client username
        forum (ForumThread): objec that store all forum data
    Returns:
        response(encoded str): response on edit message command
    """
    thread_title, message_number, message = args[0], int(args[1]), args[2]
    user_issue_command(username, "EDT")
    return forum.edit_message(thread_title, message_number, message, username)


def lst_handler(username, forum):
    """handle lsit thread  command
    Args:
        username (str): client username
        forum (ForumThread): objec that store all forum data
    Returns:
        response(encoded str): response on list thread
    """
    user_issue_command(username, "LST")
    return forum.list_threads()


def rdt_handler(args, username, forum):
    """handle read thread  command
    Args:
        args (list): argument for command
        username (str): client username
        forum (ForumThread): objec that store all forum data
    Returns:
        response(encoded str): response on read thread
    """
    thread_title = args[0]
    user_issue_command(username, "RDT")
    return forum.read_thread(thread_title)


def rmv_handler(args,  username, forum):
    """handle remove thread command
    Args:
        args (list): argument for command
        username (str): client username
        forum (ForumThread): objec that store all forum data
    Returns:
        response(encoded str): response on removing thread
    """
    thread_title = args[0]
    user_issue_command(username, "RMV")
    return forum.remove_thread(thread_title, username)


def upd_handler(serverSocket, tcpServerSocket, serverAddress, clientAddress, args, username, forum):
    """handle updlaod request from the client

    Args:
        serverSocket (socket): udp socket of server
        tcpServerSocket (socket): tcp socket of server
        serverAddress (list): addrress and port number of server
        clientAddress (list): address and port numebr of client
        args (list): arguments for the server
        username: username of client that send the data
        forum(ForumThreads): object that store all information about forum

    """
    # if already bind you don't need to bind again
    thread_title, file_name = args[0], args[1]
    file_path = find_file_path(args)

    response = forum.upload_file(thread_title, file_name, username)
    send_response(serverSocket, clientAddress, response)
    # exit if response is not upload file

    # use if statement to check if we should open a socket
    tcpServerSocket.listen(1)
    packet = recieving_file(tcpServerSocket)
    with open(file_path, 'wb') as f:
        f.write(packet)

    forum.update_forum_files(thread_title)
    print(f"{username} uploaded file {file_name} to {thread_title} thread")


def dwn_handler(serverSocket, tcpServerSocket, serverAddress, clientAddress, args, username, forum):
    print("start download")
    """handle the download command from the client

    Args:
        serverSocket (socket): udp socket of server
        tcpServerSocket (socket): tcp socket of server
        serverAddress (list): addrress and port number of server
        clientAddress (list): address and port numebr of client
        args (list): arguments for the server
        username(str): username of client that send the data
        forum(ForumThreads): object that store all information about forum
    """
    thread_title, file_name = args[0], args[1]
    file_path = find_file_path(args)

    response = forum.download_file(thread_title, file_name, username)
    send_response(serverSocket, clientAddress, response)

    tcpServerSocket.listen(1)

    tcpConnectionSocket, clientAddress = tcpServerSocket.accept()
    with open(file_path, 'rb') as file:
        download_file = file.read()

    tcpConnectionSocket.sendall(len(download_file).to_bytes(8, 'big'))
    tcpConnectionSocket.sendall(download_file)

    tcpConnectionSocket.close()
    forum.update_forum_files(thread_title)
    print(f"{file_name} downloaded from Thread {thread_title}")
    # file_path = find_download_path(args)


def recieving_file(tcpServerSocket):
    """recive file by tcp socket

    Args:
        tcpServerSocket (socket): tcp socket of server

    Returns:
        packet(file_data): file recived from the socket
    """
    tcpConnectionSocket, clientAddress = tcpServerSocket.accept()
    expected_size = b""
    while len(expected_size) < 8:
        more_size = tcpConnectionSocket.recv(9 - len(expected_size))
        expected_size += more_size

    expected_size = int.from_bytes(expected_size, 'big')
    packet = b""
    while len(packet) < expected_size:
        buffer = tcpConnectionSocket.recv(expected_size - len(packet))
        packet += buffer
    tcpConnectionSocket.close()
    return packet


def user_issue_command(username, command):
    print(f"{username} issued {command} command")


def find_file_path(args):
    thread_title, file_name = args[0], args[1]
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, f"../{thread_title}-{file_name}")


def request_parse(request):
    return request["command"], request["args"], request["credential"]
