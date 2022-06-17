from hashlib import new
from bin.utils import *


class Auth_data:
    def __init__(self):
        """
        create list to store clients and accounts
        """
        self.active_clients = []
        self.accounts = []
        self.authenticating_clients = []

    def fectching_account(self):
        """
        fetching account data from credentials.txt and stroe in accounts
        """
        f = open("credentials.txt")
        data = f.read()
        accounts = data.split("\n")
        for account in accounts:
            try:
                username, password = account.split(" ")
                self.accounts.append(Account(username, password))
            except:
                pass

    def update_account_file(self):
        """
        update the account file by using the current data stored
        """
        account_str = ""
        for account in self.accounts:
            account_str += f"{account.username} {account.password}\n"

        with open('credentials.txt', 'w') as f:
            f.write(account_str)


'''
class represent client in the application
- contain username and clientAddress
'''


class Client:

    def __init__(self, username, clientAddress):
        """
        create new client
        Args:
            username (string): username of a client
            clientAddress (list()): address that user use to authenticate
        """
        self.clientAddress = clientAddress
        self.username = username

    def __eq__(self, other):
        """check if two client is the same

        Args:
            other (Client):  another client

        Returns:
            bool: if is the same client
        """
        return (self.clientAddress == other.clientAddress and self.username == other.username)


'''
class represent account in application
- contain username and password of the account
'''


class Account:

    def __init__(self, username, password):
        """create account with username and password

        Args:
            username (string): username of an account
            password (string): password of an account
        """
        self.username = username
        self.password = password

    def __eq__(self, other):
        """check if two account are the same

        Args:
            other (Account): another account

        Returns:
            bool: if two accounts are the same
        """
        return (self.username == other.username and self.password == other.password)


def process_authentication(clientSocket, serverAddress):
    """authenticate user using their clientSocket by communicate to server via serverAddress

    Args:
        clientSocket (Socket): socket that client use to communicate with server
        serverAddress (list()): informations about server address

    Returns:
        authenticated_username: username for a user that alreadu authenticated
    """
    authenticated = None

    while not authenticated:
        username = input("Enter username: ")
        request = create_request("username_check", None, username, None)
        response = udp_communication(request, clientSocket, serverAddress)

        if response["command"] == "user already logged in":
            print(response["message"])
            continue

        password = input("Enter password: ")
        request = create_request("password_check", None, password, None)
        response = udp_communication(request, clientSocket, serverAddress)

        print(response["message"])
        if response["credential"]:
            authenticated = response["credential"]
        #  we can encapsualte this
    return authenticated 


def username_check(request, clientAddress, auth_data):
    """check username with the existed authentication database

    Args:
        request (dict): user request
        clientAddress (list): address and port numebr of client
        auth_data (Auth_data): object that store authentication related data

    Returns:
        response(encoded str): response from the server about client username
    """
    username = request["message"]

    for client in auth_data.active_clients:
        if username == client.username:
            return create_response("user already logged in", None, f"{username} is already logged in", None)

    if not is_client_active(clientAddress, auth_data):
        print("Client authenticating")

    add_authenticating_client(username, clientAddress, auth_data)
    return create_response("request password", None, None, None)


def password_check(request, clientAddress, auth_data):
    """check password from client after recieving the username

    Args:
        request (dict): request from the client
        clientAddress (list): address and port numebr of client
        auth_data (Auth_data): obeject that store authentication related data

    Returns:
        response(encoded str): response from the server about client password
    """
    username = get_username_from_authenticating(clientAddress, auth_data)
    password = request["message"]

    response = None
    if address_already_loggedin(clientAddress, auth_data):
        response = create_response(
            "Welcome to Forum", username, "Welcome to Forum", None)

    elif username_already_logged_in(username, auth_data):
        response = create_response(
            "user already logged in", None, f"{username} is already logged in", None)

    elif not_register_account(username, auth_data):
        response = create_new_account(
            username, password, clientAddress, auth_data)

    elif is_credential_valid(username, password, auth_data):
        response = login_client(username, password, clientAddress, auth_data)

    else:  # incorrect password
        print("Incorrect password")
        response = create_response(
            "incorrect_password", None, "incorrrect password", None)

    return response


def not_register_account(username, auth_data):
    """check if username is already registered as account

    Args:
        username (str): client username
        auth_data (Auth_data): object that store authentication related data

    Returns:
        bool: if username is alreadu registereed as account
    """
    return not any(account.username == username for account in auth_data.accounts)


def address_already_loggedin(clientAddress, auth_data):
    """check if clientAddress is already used to logged in

    Args:
        clientAddress (list):contain clientAddress information
        auth_data (Auth_data): object that store authentication related data

    Returns:
        bool: if clientAddress already  logged in
    """
    return any(client.clientAddress == clientAddress for client in auth_data.active_clients)


def username_already_logged_in(username, auth_data):
    """check if username is already used to logged in

    Args:
        username (str): client username
        auth_data (Auth_data): object that store authentication related data

    Returns:
        bool: if clientAddress already  logged in
    """
    return any(client.username == username for client in auth_data.active_clients)


def is_credential_valid(username, password, auth_data):
    """check if username and password is valid

    Args:
        username (str): client username
        password (str): client password
        auth_data (Auth_data): object that store authentication related data

    Returns:
        bool: if username and password valid credentials
    """
    return any((account.username == username and account.password == password) for account in auth_data.accounts)


def remove_from_authenticating(clientAddress, auth_data):
    """remove client with clientAddrss from the authenticating client list

    Args:
        clientAddress (list): address and port numebr of client
        auth_data (Auth_data): object that store authentication related data
    """
    auth_data.authenticating_clients = [
        client for client in auth_data.authenticating_clients if client.clientAddress != clientAddress]


def create_new_account(username, password, clientAddress, auth_data):
    """create new account and add to the database

    Args:
        username (string): username of client
        password (password): password of client
        clientAddress (list): address and port number of client
        auth_data (Auth_data): object that store authentication related data

    Returns:
        response (encoded string): response on creating new account
    """
    new_account = Account(username, password)
    auth_data.accounts.append(new_account)

    newClient = Client(username, clientAddress)
    auth_data.active_clients.append(newClient)

    remove_from_authenticating(clientAddress, auth_data)
    print(f"{username} successful login")

    auth_data.update_account_file()
    return create_response("Welcome to Forum", username, "Welcome to Forum", None)


def login_client(username, password, clientAddress, auth_data):
    """login client with username password and client address and add to the authentication data

    Args:
        username (str): client username
        password (str): client password
        clientAddress (list): address and port number of client
        auth_data (Auth_data): object that store authentication related data

    Returns:
        response(encoded string): response on loggging in client
    """
    newClient = Client(username, clientAddress)
    auth_data.active_clients.append(newClient)

    newAccont = Account(username, password)
    auth_data.accounts.append(newAccont)

    remove_from_authenticating(clientAddress, auth_data)

    print(f"{username} successful login")
    return create_response(
        "Welcome to Forum", username, "Welcome to Forum", None)


def get_username_from_authenticating(clientAddress, auth_data):
    """get username of matching authenticating client with the same clientAddress

    Args:
        clientAddress (list): address and port number of client
        auth_data (Auth_data): object that store authentication related data

    Returns:
        username: username of client with the same clientAddress
    """
    for client in auth_data.authenticating_clients:
        if client.clientAddress == clientAddress:
            return client.username
    return None


def add_authenticating_client(username, clientAddress, auth_data):
    """add client to list of authenticating client

    Args:
        username (username): username of client
        clientAddress (list): address and port number of client
        auth_data (Auth_data): object that store authencation related data
    """
    remove_from_authenticating(clientAddress, auth_data)
    auth_data.authenticating_clients.append(Client(username, clientAddress))


def logout_user(request, clientAddress, auth_data):
    """logout user from the sytem and active clients

    Args:
        request (dict): request from the user
        clientAddress (list): address and port number of client
        auth_data (Auth_data): object that store authentication related data

    Returns:
        _type_: _description_
    """
    username = request["credential"]
    auth_data.active_clients = [
        client for client in auth_data.authenticating_clients if client != (username, clientAddress)]
    print(f"{username} exited")
    is_waiting_for_clients(auth_data)
    return create_response("logout", None, None, None)


def is_client_active(clientAddress, auth_data):
    """check if there  is active client with matching clientAddress

    Args:
        clientAddress (_tylistpe_): address and port number of client
        auth_data (Auth_data): object that store authentication related data

    Returns:
        _type_: _description_
    """
    return any(client for client in auth_data.authenticating_clients if client.clientAddress == clientAddress)


def is_waiting_for_clients(auth_data):
    """check if there is a active_clients in the system

    Args:
        auth_data (Auth_data): object that store authenticatoin related data
    """
    n_active_clients = len(auth_data.active_clients)
    if n_active_clients == 0:
        print("Waiting for clients")
