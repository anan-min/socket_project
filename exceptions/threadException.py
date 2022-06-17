class ForumThreadException(Exception):
    pass

class ForumThreadsException(Exception):
    pass

class message_not_exists(ForumThreadException):
    pass

class user_message_access_denied(ForumThreadException):
    pass




class thread_not_exists(ForumThreadsException):
    pass
class thread_already_exists(ForumThreadsException):
    pass
class user_thread_access_denied(ForumThreadsException):
    pass





