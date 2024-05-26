import yaml
from yaml.loader import SafeLoader

def load_commands(commands_file_path):
    """Parses the Commands files representing the known commands for Alvin
    """
    with open(commands_file_path, 'r') as input_file:
        command_strings = yaml.load(
            input_file, 
            Loader = SafeLoader
        )

    return command_strings