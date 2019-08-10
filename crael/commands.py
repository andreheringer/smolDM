"""
    This module implements the central command handling object.

    :copywrite: Andre Heringer 2018
    :license: MIT, see license for details
"""
import re


class CommandHandler:
    """A class created with the intention to help make butler commands easy to write."""

    def __init__(self):
        """
            CommandHandler __init__ method.
        """

        # :list of tuple: (command_regular_expression, function_signature)
        self.command_list = []

        # :dic of fuction: Dictionary key->function_signature
        self.error_handlers = dict()

    @staticmethod
    def build_command_pattern(command: str):
        """Function used to build the regex which will be matche agains user input.

            Parameters:
                command: The command string used for registration.

            Returns:
                The regular expresison generated.
        """

        # swap every expression wiht the format <vaiable> to ?Pvariable
        # this way the .match method from re can be called
        command_regex = re.sub(r"(<\w+>)", r"(?P\1.+)", command)
        return re.compile(f"^{command_regex}$")

    def register(self, command_str: str):
        """Register method decorator witch binds the function to the command regex.

            Parameters:
                command_str: the command string which will be used to resgister the function under

            Retruns:
                The decorated function reference.
        """

        def command_decorator(func):
            command_patter = self.build_command_pattern(command_str)
            self.command_list.append((command_patter, func))
            return func

        return command_decorator

    def get_command_match(self, message):
        """This method searches for a command match in the command_list atribute.

            Parameters:
                message: message object from the Dsicord API

            Returns:
                optinal tuple: A tuple containing the match dictionary and the function reference
        """
        command = message.content  # get the text in message
        for command_patter, command_func in self.command_list:
            match = command_patter.match(command)
            if match:
                return match.groupdict(), command_func

        return None

    def cmd_not_found(self):
        """Helper decorator for resgistering a command match faill back function.

            **Does not accept any parameters**

            Returns:
                The decorated function
        """

        def cmd_error_decorator(func):
            self.error_handlers.update({"cmd_not_found": func})
            return func

        return cmd_error_decorator
