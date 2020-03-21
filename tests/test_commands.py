from unittest import mock
import pytest
from smolDM.commands import CommandHandler


# Constants
STR_COMMAND = "!this"
STR_COMMAND_WITH_VARIABLE = "!this <number>"
STR_INPUT = "!this"
STR_INPUT_WITH_VARIABLE = "!this 20"

mock_message = mock.Mock(content=STR_INPUT)

# Pytest fixture and sample functions used for tests
@pytest.fixture
def bot_instance():
    bot = CommandHandler()
    return bot


def sample_func():
    return f"Horray!"


def sample_func_with_variable(number):
    return f"Horray! With {number}!"


def sample_error_handler():
    return f"Opszy..."


# Actual tests start here
def test_build_comand_pattern():
    input_str = STR_INPUT
    initial_str_command = STR_COMMAND
    new_command = CommandHandler.build_command_pattern(initial_str_command)
    assert new_command.match(input_str)


def test_register(bot_instance):
    # Check if the initial command_list is empty
    assert len(bot_instance.command_list) == 0
    # Try to register a new command
    register_decorator = bot_instance.register(STR_COMMAND)
    _ = register_decorator(sample_func)
    # See if the command_list increased by 1
    assert len(bot_instance.command_list) == 1
    # Register a new function with a variable
    register_decorator = bot_instance.register(STR_COMMAND_WITH_VARIABLE)
    _ = register_decorator(STR_INPUT_WITH_VARIABLE)
    assert len(bot_instance.command_list) == 2


def test_get_command_match(bot_instance):
    register_decorator = bot_instance.register(STR_COMMAND)
    _ = register_decorator(sample_func)
    assert bot_instance.get_command_match(mock_message)

    mock_message.configure_mock(content=STR_INPUT_WITH_VARIABLE)
    register_decorator = bot_instance.register(STR_COMMAND_WITH_VARIABLE)
    _ = register_decorator(sample_func_with_variable)
    assert bot_instance.get_command_match(mock_message)


def test_cmd_not_found(bot_instance):
    assert not any(bot_instance.error_handlers)
    register_decorator = bot_instance.cmd_not_found()
    _ = register_decorator(sample_error_handler)
    assert bot_instance.error_handlers["cmd_not_found"] is sample_error_handler
