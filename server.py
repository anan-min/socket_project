from socket import *
from lib.requestHandlerThread import RequestHanlderThread
from bin.utils import *
from lib.forumData import *
from bin.response import *
from lib.requestHandler import *
import sys


# acquire server host and port from command line parameter
if len(sys.argv) != 2:
    print("\n===== Error usage, python3 TCPServer3.py SERVER_PORT ======\n")
    exit(0)

serverHost = "127.0.0.1"
serverPort = int(sys.argv[1])
serverAddress = (serverHost, serverPort)
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddress)

tcpServerSocket = socket(AF_INET, SOCK_STREAM)
tcpServerSocket.bind(serverAddress)

# auth_data = Auth_data()
# forum = Forum_threads()
# fectching_account(auth_data)
data = ForumData()


# we could create db that is a class that handle everything related to the data
# this will encapsulte some of the par that we don't want  to expose  to the system
'''
generate and send response to client determined by request
and client server
'''


print(f"Server is listening on port {serverPort} address {serverHost}")
print(f"Waiting for clients")
while True:
    # recieve request from the clietn
    request, clientAddress = serverSocket.recvfrom(2048)
    # create thread to handle with the request
    handlerThread = RequestHanlderThread(
        request, serverSocket, tcpServerSocket, clientAddress, serverAddress, data)
    handlerThread.start()
