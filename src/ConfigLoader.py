import os

class ConfigLoader():
    """
    Attempt to load config
    """
    DEFAULT_CONFIG_LOCATION='/Users/robertgame/.meetup-rss.conf'

    def __init__(self):
        """_summary_

        Raises:
            FileNotFoundError: _description_
        """
        self.config = self.load_config_from_file(self.DEFAULT_CONFIG_LOCATION)
    
    def load_config_from_file(self, config_location):
        """_summary_
        """
        config_file_path = config_location

        # Using readlines()
        config_file = open(config_file_path, 'r', encoding="UTF-8")
        config_file_lines = config_file.readlines()
        config_file.close()
        
        # Strips the newline character
        config = []
        for config_file_line in config_file_lines:
            config_line_clean = config_file_line.strip()
            config.append(config_line_clean)

        return config

    def get_config(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.config

    def __str__(self):
        return "Config loaded from file"