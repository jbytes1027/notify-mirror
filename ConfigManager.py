import pathlib
import configparser

DEFAULT_CONFIG_PATH = "~/.config/notify-sync.ini"


class ConfigManager:
    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.config = configparser.ConfigParser()

        path = pathlib.PosixPath(self.config_path).expanduser()

        if path.exists():
            # read config file
            with open(path, "r") as config_file:
                self.config.read_file(config_file)
        else:
            if not path.parent.exists():
                # create config dir
                path.parent.mkdir(parents=True)

            # set default settings
            self.config["GENERAL"] = {
                "api_key": "",
                "notify_on_error": "no",
                "notify_on_connection_changed": "no",
            }

            self.config["DEFAULT NOTIFICATION"] = {
                "icon": "given",
                "timeout": "default",
                "urgency": "default",
                "exec_on_click": "",
            }

            # create config file
            with open(path, "w") as config_file:
                self.config.write(config_file)

    def get_ephemeral_setting(self, ephemeral, setting):
        if (
            ephemeral["package_name"] in self.config
            and setting in self.config[ephemeral["package_name"]]
        ):
            return self.config[ephemeral["package_name"]][setting]
        else:
            return self.config["DEFAULT NOTIFICATION"][setting]

    def get_api_key(self):
        return self.config["GENERAL"]["api_key"]
