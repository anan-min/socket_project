def create_response(command, credential, message, args):
    """create encoded string for sending in the udp or tcp connection

    Args:
        command (_type_): _description_
        credential (_type_): _description_
        message (_type_): _description_
        args (_type_): _description_

    Returns:
        _type_: _description_
    """
    reseponse_obj = {
        'command': command,
        'credential': credential,
        'message': message,
        'args': args
    }
    return str(reseponse_obj).encode()


def udp_message_to_obj(request):
    """convert message from udp connection to request obj which is a dict

    Args:
        request (encoded str): request in form of encoded string from UDP/TCP connection

    Returns:
        (dict): object that contain info in request
    """
    return eval(request.decode())


def response_to_obj(response):
    """convert response as encodedn string to a dict object

    Args:
        response (encoded str): response from the server

    Returns:
        dict: object that store content from the response
    """
    return eval(response.decode())


def udp_communication(message, clientSocket, serverAddress):
    """send message to serverAddress using clientSocket via UDP communication

    Args:
        message (str): message that client atttempt to send
        clientSocket (_type_): _description_
        serverAddress (_type_): _description_

    Returns:
        _type_: _description_
    """
    response = None
    while not response:
        clientSocket.sendto(message, serverAddress)
        response, serverAddress = clientSocket.recvfrom(2048)
    return response_to_obj(response)


def create_request(command, credential, message, args):
    """create request from the commadn, credential, message and arsg

    Args:
        command (str): command that user request
        credential (str): credential of user or a username
        message (str): message from a user
        args (list): args for command

    Returns:
        (encode str): encoded string represntation of dict that store info
    """
    request_dict = {
        'command': command,
        'credential': credential,
        'message': message,
        'args': args
    }
    return str(request_dict).encode()


def get_credentials(response):
    return response["credential"]


def client_exit():
    print("Goodbye")


