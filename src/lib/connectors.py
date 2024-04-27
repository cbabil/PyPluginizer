import logging
from codetiming import Timer
import importlib.util

logger = logging.getLogger(__name__)


@Timer(name="Import connector",
       text="{name} finished in {:.4f} seconds...",
       logger=logging.info)
def import_module(connector):
    try:
        # import module
        moduleFile = importlib.util.spec_from_file_location(connector, "src/connectors/" + connector + "/__main__.py")
        module = importlib.util.module_from_spec(moduleFile)
        moduleFile.loader.exec_module(module)
        logger.info("Loaded connector %s version %s", connector, module.__version__)
    except (ImportError, FileNotFoundError):
        logging.error("Connector not found: %s", connector)
        return
    except (AttributeError) as err:
        logging.error("Cannot load connector: %s: %s", connector, err)
        return
    return module
