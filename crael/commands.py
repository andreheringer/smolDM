"""
    This module implements the central command handling object.

    :copywrite: Andre Heringer 2018
    :license: MIT, see license for details
"""
import re


class CommandHandler:
    """This class handles commnand parsing."""

    def __init__(self):
        """Command Handler __init__ method."""
        # :list of tuple: (command_regular_expression, function_signature)
        self.command_list = []

        # :dic of fuction: Dictionary key->function_signature
        self.error_handlers = dict()

    @staticmethod
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

    def register(self, command_str: str) -> callable:
        """Register method decorator witch binds the function to the command regex.

        Args:
            command_str: the command string which will be used to resgister
                         the function under

        Returns:
            The decorated function reference.

        """

        def command_decorator(func: callable) -> callable:
            command_patter = self.build_command_pattern(command_str)
            self.command_list.append((command_patter, func))
            return func

        return command_decorator

    def get_command_match(self, message: str):
        """Find an registered command that matches pattern on message.

        Args:
            message: message object from the Discord API

        Returns:
            optinal tuple: A tuple containing the match dictionary and the
                           function reference

        """
        command = message.content  # get the text in message
        for command_patter, command_func in self.command_list:
            match = command_patter.match(command)
            if match:
                return match.groupdict(), command_func

        return None

    def cmd_not_found(self) -> callable:
        """Decorate standard fail back function.

        **Does not accept any parameters**

        Returns:
            The decorated function

        """

        def cmd_error_decorator(func):
            self.error_handlers.update({"cmd_not_found": func})
            return func

        return cmd_error_decorator
