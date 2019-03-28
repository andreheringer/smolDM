import pytest
from src.commands import CommandHandler


# Constants
STR_COMMAND = "!this"
STR_COMMAND_WITH_VARIABLE = "!this <number>"
STR_INPUT = "!this"
STR_INPUT_WITH_VARIABLE = "!this 20"

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


"""
def test_get_command_match(bot_instance):
    register_decorator = bot_instance.register(STR_COMMAND)
    _ = register_decorator(sample_func)
    assert bot_instance.get_command_match(STR_INPUT)

    register_decorator = bot_instance.register(STR_COMMAND_WITH_VARIABLE)
    _ = register_decorator(sample_func_with_variable)
    assert bot_instance.get_command_match(STR_INPUT_WITH_VARIABLE) """


def test_cmd_not_found(bot_instance):
    assert not any(bot_instance.error_handlers)
    register_decorator = bot_instance.cmd_not_found()
    _ = register_decorator(sample_error_handler)
    assert bot_instance.error_handlers['cmd_not_found'] is sample_error_handler
