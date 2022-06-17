from lib.auth import *
from lib.fthread import *


'''
Class that represent data in forum
- auth_data stores data related to authentication
- fecthing fetch account from the credentials.txt
- forum stores data related to threads, messages, and files 
'''
class ForumData():
    def __init__(self) -> None:
        self.auth_data = Auth_data()
        self.auth_data.fectching_account()
        self.forum = Forum_threads()