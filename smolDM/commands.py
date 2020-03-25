"""
This module implements the central command handling object.

:copywrite: Andre Heringer 2018
:license: MIT, see license for details
"""
import re


def build_command_pattern(command: str):
    """Build regex pattern based on Crael command rules.

    Args:
        command: The command string used for registration

    Returns:
        The regular expresison generated.

    """
    # swap every expression wiht the format <vaiable> to ?Pvariable
    # this way the .match method from re can be called
    command_regex = re.sub(r"(<\w+>)", r"(?P\1.+)", command)
    return re.compile(f"^{command_regex}$")


def register(command_list, command_str: str) -> callable:
    """Register method decorator witch binds the function to the command regex.

    Args:
        command_str: the command string which will be used to resgister
                        the function under

    Returns:
        The decorated function reference.

    """

    def command_decorator(func: callable) -> callable:
        command_patter = build_command_pattern(command_str)
        command_list.append((command_patter, func))
        return func

    return command_decorator


def add_command(command_list, func, command_str):
    """Add a function and the command pattern to the command list.

    Args:
        func: Function it will be called
        command_str: command string that specifies the pattern

    """
    command_pattern = build_command_pattern(command_str)
    command_list.append((command_pattern, func))
    return command_list


def get_command_match(command_list, message: str):
    """Find an registered command that matches pattern on message.

    Args:
        message: message object from the Discord API

    Returns:
        optinal tuple: A tuple containing the match dictionary and the
                        function reference

    """
    command = message.content  # get the text in message

    match_list = map(
        lambda match: (match[0].match(command), match[1]), command_list
    )

    for command_patter, command_func in match_list:
        if command_patter:
            return command_patter.groupdict(), command_func

    return None


def add_special_handler(special_handlers, func, command_str, especial_key):
    """
    """
    command_pattern = build_command_pattern(command_str)
    special_handlers.update({especial_key: (command_pattern, func)})
    return special_handlers


def cmd_not_found(special_handlers) -> callable:
    """Decorate standard fail back function.

    **Does not accept any parameters**

    Returns:
        The decorated function

    """

    def cmd_error_decorator(func):
        special_handlers.update({"cmd_not_found": func})
        return func

    return cmd_error_decorator
