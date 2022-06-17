class fileTransferException(Exception):
    pass


class file_not_found(fileTransferException):
    pass


class file_already_exists(fileTransferException):
    pass
