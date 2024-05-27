import yaml
from yaml.loader import SafeLoader

def load_template_file(file_path):
    """Parses the standardized Yaml files representing the known commands for Alvin 
    or Prompts
    """
    with open(file_path, 'r') as input_file:
        template_strings = yaml.load(
            input_file, 
            Loader = SafeLoader
        )

    return template_strings