class CommandExcpetion(Exception):
    pass


class command_not_exists(CommandExcpetion):
    pass


class command_syntax_invalid(CommandExcpetion):
    pass


class client_exit_exception(CommandExcpetion):
    pass 
