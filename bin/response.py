from bin.utils import *


def thread_created_response(thread_title):
    return create_response("thread created", None, f"Thread {thread_title} created", None)


def thread_already_exists_response(thread_title):
    return create_response("thread existed", None, f"Thread {thread_title} exists", None)


def message_posted_response(thread_title):
    return create_response("message posted", None, f"Message posted to {thread_title} thread", None)


def read_empty_thread_response(thread_title):
    return create_response("thread empty", None, f"Thread {thread_title} is empty", None)


def message_edited_response():
    return create_response("message edited", None, "The message has been edited", None)


def thread_access_denied_response():
    return create_response("thread access denied", None, "The thread was created by another userand cannot be removed", None)


def thread_removed_response(thread_title):
    return create_response("thread removed", None, f"Thread {thread_title} removed", None)


def thread_not_existed_response(thread_title):
    return create_response("thread not existed", None, f"Thread {thread_title} does not exist", None)


def logout_response():
    return create_response("logout", None, "Goodbye", None)


def message_not_existed_response():
    return create_response("message_not_existed", None, "message not existed", None)


def message_delete_denied_response():
    return create_response("message access denied", None, "The message was posted by another user and cannot be removed", None)


def message_edit_denied_response():
    return create_response("message access denied", None, "The message was posted by another user and cannot be editted", None)


def read_thread_response(thread_title, forum_str):
    if not forum_str:
        return read_empty_thread_response(thread_title)

    return create_response("read thread", None, forum_str, None)


def list_thread_response(thread_titles):
    if len(thread_titles) == 0:
        return forum_empty_response()

    return create_response("list threads", None, threads_representation(thread_titles), None)


def forum_empty_response():
    return create_response("list threads", None, "No threads to list", None)


def message_delete_response():
    return create_response("message deleted", None, "The message has been deleted", None)


def file_not_existed_response(thread_title):
    return create_response("file already exists", None, "File does not exist in Thread {thread_title}", None)


def file_already_exists_response():
    return create_response("file not found", None, "File not found", None)

def upload_file_response(file_name, username, thread_title):
    args = [file_name, username]
    return create_response("upload file", None, f"{file_name} uploaded to {thread_title} thread", args)


def download_file_response(file_name, username, thread_title):
    args = [file_name, username]
    return create_response("download file", None, f"{file_name} successfully downloaded", args)


#  helper functions


def messages_representation(messages):
    """return string respresentation of the message

    Args:
        messages (list): message that user want string from

    Returns:
        _type_: _description_
    """
    message_str = ""
    for i in range(len(messages)):
        message_str += f"{i+1} {messages[i].get_author()}: {messages[i].get_message()}\n"
    return message_str.rstrip("\n")


def threads_representation(thread_titles):
    """return string representation of threads in forum

    Args:
        thread_titles (str): all thread titles from the forum

    Returns:
        str: string representation of threads in forum
    """
    threads_str = "The list of active threads:"
    for title in thread_titles:
        threads_str += f"\n{title}"
    return threads_str
