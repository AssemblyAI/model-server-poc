import yaml
import importlib
from commons import Logger
logger = Logger.get_logger(__name__)

def get_model(yaml_config):
    package = yaml_config['package']
    try:
        importlib.import_module(package)
    except Exception as e:
        logger.critical(f"package {package} is not installed, aborting")
        raise ModuleNotFoundError(package)

    engine = yaml_config['engine']
    path = engine['path'].split('.')
    module = '.'.join(path[:-1])
    cls = path[-1]
    model = getattr(importlib.import_module(module), cls)

    return model