from re import L
from threading import Thread
from lib.requestHandler import *
import os

'''
subthread of client that works on subtask while mainthread deal request and response with the user
'''


class ClientThread(Thread):

    def __init__(self, response, serverAddress):
        """_
        parameter:
            response (dict): response from the server
            serverAddress (list): contain information about server address
        return new_thread(ClientThread)
        """
        Thread.__init__(self)
        command, args = self.parse_response(response)
        self.command = command
        self.response = response
        self.serverAddress = serverAddress
        self.file_name, self.username = args

    def run(self):
        """
        perform upload and download file if the command in the response request
        for upload and download file
        """
        if self.command == "upload file":
            self.handleUpload()
        elif self.command == "download file":
            self.handleDownload()

        # request connection to the server
        # send or recieve data from the server
    def handleUpload(self):
        """
        handle with upload response from the server
        - find a file in client directory
        - initiate tcp connection
        - send file
        - display status message
        """
        # find the file
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, f"../{self.file_name}")

        with open(file_path, 'rb') as file:
            upload_file = file.read()
        # initiate tcp connection
        tcpClientSocket = socket(AF_INET, SOCK_STREAM)
        tcpClientSocket.connect(self.serverAddress)
        # send file
        tcpClientSocket.sendall(len(upload_file).to_bytes(8, 'big'))
        tcpClientSocket.sendall(upload_file)

        # display message
        self.display_message(self.response)
        file.close()

    def handleDownload(self):
        """
        - connect to tcp connection
        - recive data and store in buffer
        - save in file_name that sended in the response
        """
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, f"../{self.file_name}")

        tcpClientSocket = socket(AF_INET, SOCK_STREAM)
        tcpClientSocket.connect(self.serverAddress)

        expected_size = b""
        while len(expected_size) < 8:
            more_size = tcpClientSocket.recv(9 - len(expected_size))
            expected_size += more_size

        expected_size = int.from_bytes(expected_size, 'big')
        packet = b""
        while len(packet) < expected_size:
            buffer = tcpClientSocket.recv(expected_size - len(packet))
            packet += buffer

        with open(file_path, 'wb') as file:
            file.write(packet)

        self.display_message(self.response)
        file.close

    def parse_response(self, response):
        """_summary_

        Args:
            response (dict): reponse from the server

        Returns:
            (string, list(string)): command and args
        """
        return response["command"], response["args"]

    def display_message(self, response):
        """
        display message that sended by the server
        """
        message = response["message"]
        if message:
            print(f"\n{message}")


