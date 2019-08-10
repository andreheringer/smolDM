import json
import os
from collections import namedtuple

ConfigDev = namedtuple("ConfigDev", "DiscordBotToken DatabaseFile Schema")


def load_config(config_file, env="dev"):
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), config_file)
    with open(config_path) as file:
        new_env = json.load(file)
        if env == "dev":
            dev_env = ConfigDev(**new_env)
            return dev_env


dev_env = load_config("config/config.json")
