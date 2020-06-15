import os
import logging.config
import yaml

from settings import PROJECT_ROOT


def setup_logging(
    default_path='logging_config.yaml',
    default_level=logging.INFO
):
    """
    Setup logging configuration
    """
    path = default_path
    config_path = os.path.join(PROJECT_ROOT, path)
    if os.path.exists(config_path):
        with open(config_path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
