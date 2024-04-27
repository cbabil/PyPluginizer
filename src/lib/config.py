import logging
import yaml

logger = logging.getLogger(__name__)


def yaml_parser(file_path: str):
    """Parse YAML data from a file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict or None: The parsed YAML data if successful, None otherwise.
    """
    try:
        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
            return yaml_data
    except FileNotFoundError:
        logger.error("File {} not found.".format(file_path))
        return None
    except PermissionError:
        logger.error("You do not have permission to open the file {}.".format(file_path))
        return None
    except yaml.YAMLError as e:
        if hasattr(e, 'context_mark') and isinstance(e.context_mark, yaml.Mark):
            mark = e.context_mark
            logger.error("Error: An error occurred while parsing the YAML file at line: {}, column: {}".format(mark.line + 1, mark.column + 1))
        elif hasattr(e, 'context'):
            logger.error("Error: An error occurred while parsing the YAML file: {}".format(e.context))
            logger.error("Error context: {}".format(e.problem))
        else:
            logger.error("Error: An error occurred while parsing the YAML file: {}".format(e))
        return None
    except Exception as e:
        logger.error("Error: An unexpected error occurred while parsing the YAML file {}: {}".format(file_path, e))
        return None
