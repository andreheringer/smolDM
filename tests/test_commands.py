from unittest import mock
import pytest
import smolDM.commands as cmd


# Constants
STR_COMMAND = "!this"
STR_COMMAND_WITH_VARIABLE = "!this <number>"
STR_INPUT = "!this"
STR_INPUT_WITH_VARIABLE = "!this 20"

mock_message = mock.Mock(content=STR_INPUT)


def sample_func():
    return f"Horray!"

def sample_com():
    return f"WOW!"

def sample_func_with_variable(number):
    return f"Horray! With {number}!"


def sample_error_handler():
    return f"Opszy..."


# Actual tests start here
def test_build_comand_pattern():
    input_str = STR_INPUT
    initial_str_command = STR_COMMAND
    new_command = cmd.build_command_pattern(initial_str_command)
    assert new_command.match(input_str)


def test_register():
    commands = []
    # Try to register a new command
    register_decorator = cmd.register(commands, STR_COMMAND)
    _ = register_decorator(sample_func)
    # See if the command_list increased by 1
    assert len(commands) == 1
    # Register a new function with a variable
    register_decorator = cmd.register(commands, STR_COMMAND_WITH_VARIABLE)
    _ = register_decorator(sample_func_with_variable)
    assert len(commands) == 2


def test_get_command_match():
    commands = []
    register_decorator = cmd.register(commands, STR_COMMAND)
    _ = register_decorator(sample_func)
    assert cmd.get_command_match(commands, mock_message)

    mock_message.configure_mock(content=STR_INPUT_WITH_VARIABLE)
    register_decorator = cmd.register(commands, STR_COMMAND_WITH_VARIABLE)
    _ = register_decorator(sample_func_with_variable)
    assert cmd.get_command_match(commands, mock_message)


def test_get_command_dont_match():
    commands = []
    register_decorator = cmd.register(commands, STR_COMMAND)
    _ = register_decorator(sample_func)
    mock_message.configure_mock(content="!Should not work")
    assert cmd.get_command_match(commands, mock_message) is None


def test_add_command():
    commands = []
    message = mock.Mock(content="!wow")
    commands = cmd.add_command(commands, sample_com, "!wow")
    assert cmd.get_command_match(commands, message)
