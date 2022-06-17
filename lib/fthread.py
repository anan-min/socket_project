from email import message
from exceptions.fileException import file_already_exists, file_not_found
from exceptions.threadException import *
from bin.response import *
from bin.utils import *
from socket import *
import os

'''
class that represent message in thread
'''


class Thread_message:
    def __init__(self, message, username):
        self.message = message
        self.username = username

    def get_message(self):
        return self.message

    def get_author(self):
        return self.username

    def set_message(self, message):
        self.message = message

    def __repr__(self):
        return f"{self.message} {self.username}"

# message number should be index +  1/ size + 1


'''
class that represent a thread in forum
'''


class Forum_Thread():
    def __init__(self, thread_title, username):
        self.thread_title = thread_title
        self.username = username
        self.messages = list()
        self.file_names = []

    def __eq__(self, other):
        return self.thread_title == other.thread_title and self.username == other.username

    def __repr__(self):
        return f"{self.thread_title} {self.username} {self.messages}"

    def post_message(self, message, username):
        """post user message to the thread

        Args:
            message (str): user message
            username (str): client username
        """
        newMessage = Thread_message(message, username)
        self.add_message(newMessage)

    def delete_message(self, message_number, username):
        """delete message in a thrad

        Args:
            message_number (int): message number of deleting message
            username (str): client username
        """
        self.validate_user(message_number, username)
        self.messages.pop(message_number - 1)

    def edit_message(self, message_number, message, username):
        """edit message at message number specified with new message

        Args:
            message_number (int): message of deleting message
            message (str): edited message
            username (str): client username

        """
        self.validate_user(message_number, username)
        edit_message = self.messages[message_number - 1]
        edit_message.set_message(message)

    def read_thread(self):
        """read thread andd return string  represent forum

        Returns:
            (str) : string represent forum
        """
        if len(self.messages) == 0 and len(self.file_names) == 0:
            return None

        forum_str = ""
        forum_str += f"{self.username}\n"
        for i in range(len(self.messages)):
            forum_str += f"{i+1} {self.messages[i].get_author()}: {self.messages[i].get_message()}\n"
        for file in self.file_names:
            username, file_name = file
            forum_str += f"{username} uploaded {file_name}"
        return forum_str

    # file transfer

    def upload_file(self, file_name, username):
        """get respone for uploading file with file name from the client with specified username

        Args:
            file_name (str): uploding file
            username (str): client username

        Raises:
            file_already_exists: file already exists in thread

        Returns:
            _type_: _description_
        """
        if file_name in self.file_names:
            raise file_already_exists
        self.file_names.append((username, file_name))
        return upload_file_response(file_name, username, self.thread_title)

    def download_file(self, file_name, username):
        print("fthread download file")
        for data in self.file_names:
            d_username, d_file_name = data
            if file_name == d_file_name:
                return download_file_response(file_name, username, self.thread_title)

        raise file_not_found

    # getter functions

    def add_message(self, message):
        """adsd message to the thread message lsit

        Args:
            message (str): message to add
        """
        self.messages.append(message)

    def get_threadtitle(self):
        return self.thread_title

    def get_author(self):
        return self.username

    def is_valid_message_number(self, message_number):
        """check if it is valid message number for the thread

        Args:
            message_number (int): message number to validate

        Returns (bool): if message number validate
        """
        return message_number >= 1 and message_number <= len(self.messages)

    def validate_user(self, message_number, username):
        """validate user if user have access to the message with message number

        Args:
            message_number (int): message number that use to check access
            username (str): _description_

        Raises:
            message_not_exists: message is not exists in the thread
            user_message_access_denied: user does not have persmission for message
        """
        if not self.is_valid_message_number(message_number):
            raise message_not_exists

        message = self.messages[message_number - 1]
        if message.get_author() != username:
            raise user_message_access_denied

    def update_forum_file(self):
        """update file that contain forum information
        """
        forum_str = ""
        forum_str += f"{self.username}\n"
        for i in range(len(self.messages)):
            forum_str += f"{i+1} {self.messages[i].get_author()}: {self.messages[i].get_message()}\n"
        for file in self.file_names:
            username, file_name = file
            forum_str += f"{username} uploaded {file_name}"

        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, f"../{self.thread_title}")
        with open(file_path, 'w') as file:
            file.write(forum_str)


'''
class that represent forum
'''


class Forum_threads():
    def __init__(self):
        self.thread_lists = []

    def create_thread(self, thread_title, username):
        """create thread and add to thread list in the forum

        Args:
            thread_title (str): thread title name
            username (str): client username

        Returns:
            response(encoded str): response for creating thread
        """
        try:
            self.check_existed_thread(thread_title)
            newThread = Forum_Thread(thread_title, username)
            self.thread_lists.append(newThread)
            self.update_forum_files(thread_title)
            print(f"Thread {thread_title} created")
            return thread_created_response(thread_title)
        except thread_already_exists:
            return thread_already_exists_response(thread_title)

    def post_message(self, thread_title, message, username):
        """ post message to thread with thread title

        Args:
            thread_title (str): thread that user attempt to post message on
            message (str): user message
            username (_type_): client username

        Returns:
            reponse(encoded str): response from posting message on the thread
        """
        try:
            thread = self.find_thread(thread_title)
            messages = thread.post_message(message, username)
            self.update_forum_files(thread_title)
            return message_posted_response(thread_title)
        except thread_not_exists:
            return thread_not_existed_response(thread_title)

    def delete_message(self, thread_title, message_number, username):
        """delete message with message_number* on thread with thread_tiile*

        Args:
            thread_title (str): thread title of target thread
            message_number (int): message  number of deleting message
            username (str): client username

        Returns:
            response(encoded str): response for deleting message
        """
        try:
            thread = self.find_thread(thread_title)
            thread.delete_message(message_number, username)
            print("message deleted")
            self.update_forum_files(thread_title)
            return message_delete_response()
        except thread_not_exists:
            return thread_not_existed_response(thread_title)
        except message_not_exists:
            return message_not_existed_response()
        except user_message_access_denied:
            return message_delete_denied_response()

    def edit_message(self, thread_title, message_number, message, username):
        """edit message on the thread with ~

        Args:
            thread_title (_type_): _description_
            message_number (_type_): _description_
            message (_type_): _description_
            username (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            thread = self.find_thread(thread_title)
            thread.edit_message(message_number, message, username)
            print("The message has been edited")
            self.update_forum_files(thread_title)
            return message_edited_response()
        except thread_not_exists:
            return thread_not_existed_response(thread_title)
        except message_not_exists:
            return message_not_existed_response()
        except user_message_access_denied:
            return message_edit_denied_response()

    def list_threads(self):
        """list thread_title of all thread in the forum

        Returns:
            str: list of thread title in forum
        """
        thread_titles = [thread.get_threadtitle()
                         for thread in self.thread_lists]
        return list_thread_response(thread_titles)

    def read_thread(self, thread_title):
        """read thread that has thread title and return response about that thread

        Args:
            thread_title (_type_): _description_

        Returns:
            response(encoded str): response on reading thread
        """
        try:
            thread = self.find_thread(thread_title)
            forum_str = thread.read_thread()
            print(f"Thread {thread_title} read")
            return read_thread_response(thread_title, forum_str)
        except thread_not_exists:
            return thread_not_existed_response(thread_title)

    def remove_thread(self, thread_title, username):
        """_summary_

        Args:
            thread_title (_type_): _description_
            username (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            self.delete_thread(thread_title, username)
            print("The thread has been removed")
            self.update_forum_files(thread_title)
            return thread_removed_response(thread_title)
        except thread_not_exists:
            return thread_not_existed_response(thread_title)
        except user_thread_access_denied:
            return thread_access_denied_response()

    def upload_file(self, thread_title, file_name, username):
        """upload file with name file_name and to the thread with thread_title

        Args:
            thread_title (str): thread title of thread file uploading
            file_name (str): uploading file
            username (str): username of client that upload a file

        Returns:
            response(encoded str): response on uploading file
        """
        try:
            thread = self.find_thread(thread_title)
            thread.upload_file(file_name, username)
            return upload_file_response(file_name, username, thread_title)
        except thread_not_exists:
            return thread_not_existed_response(thread_title)
        except file_already_exists:
            return file_already_exists_response()

    def download_file(self, thread_title, file_name, username):
        """download file with file_name from thread with thread_title

        Args:
            thread_title (str): thread title of thread that downloading file from
            file_name (str): downloading file name
            username (str): username of client that download the file

        Returns:
            response(encoded str): response on downloading file
        """
        try:
            thread = self.find_thread(thread_title)
            thread.download_file(file_name, username)
            return download_file_response(file_name, username, thread_title)
        except thread_not_exists:
            return thread_not_existed_response(thread_title)
        except file_not_found:
            return file_not_existed_response(thread_title)

    # helper functions

    def delete_thread(self, thread_title, username):
        """delete thread with thread title from the forum

        Args:
            thread_title (str): thread title of deleting thread
            username (_type_): username of client that attempt to delete thread

        Raises:
            user_thread_access_denied: user does not have access to delete thread
        """
        deleted_thread = self.find_thread(thread_title)
        if deleted_thread.get_author() != username:
            raise user_thread_access_denied
        self.thread_lists = [
            fthread for fthread in self.thread_lists if fthread != deleted_thread]

    def check_existed_thread(self, thread_title):
        """check  if thread with thread_title existed in the forum

        Args:
            thread_title (str): thread title of thread that user attempt to find

        Raises:
            thread_already_exists: thread exists in the forum
        """
        if any(fthread.get_threadtitle() == thread_title for fthread in self.thread_lists):
            raise thread_already_exists

    def find_thread(self, thread_title):
        """find thread with thread title in the forum

        Args:
            thread_title (str): thread title that user want to find

        Raises:
            thread_not_exists: thread not exists in the forum

        Returns:
            thread(ForumThread): thread with thread title
        """
        for thread in self.thread_lists:
            if thread.thread_title == thread_title:
                return thread
        raise thread_not_exists

    def get_list_threads(self):
        """find list of all thread in the forum

        Returns:
            (list): list of all thread in the forum
        """
        return self.list_threads

    def update_forum_files(self, thread_title):
        """updat file that store thread inforamtion

        Args:
            thread_title (str): thread title of thread with associated file
        """
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, f"../{thread_title}")

        try:
            thread = self.find_thread(thread_title)
            thread.update_forum_file()
        except thread_not_exists:
            os.remove(file_path)
