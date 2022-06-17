from threading import Thread
from lib.requestHandler import *


'''
class represent thread that handle request from the server
'''
class RequestHanlderThread(Thread):
    def __init__(self, request, serverSocket, tcpServerSocket, clientAddress, serverAddress, data):
        Thread.__init__(self)
        self.request = request
        self.serverSocket = serverSocket
        self.tcpServerSocket = tcpServerSocket
        self.clientAddress = clientAddress
        self.serverAddress = serverAddress
        self.data = data

    def run(self):
        requestHandler(self.request, self.serverSocket, self.tcpServerSocket,
                       self.clientAddress, self.serverAddress, self.data)
