import logging
from codetiming import Timer
import importlib.util

logger = logging.getLogger(__name__)


@Timer(name="Import scanner",
       text="{name} finished in {:.4f} seconds...",
       logger=logging.info)
def import_module(scanner):
    try:
        # import module
        moduleFile = importlib.util.spec_from_file_location(scanner, "src/plugins/scanners/" + scanner + "/__main__.py")
        module = importlib.util.module_from_spec(moduleFile)
        moduleFile.loader.exec_module(module)
        logger.info("Loaded scanner %s version %s", scanner, module.__version__)
    except (ImportError, FileNotFoundError):
        logging.error("Scanner not found: %s", scanner)
        return
    except (AttributeError) as err:
        logging.error("Cannot load scanner: %s: %s", scanner, err)
        return
    return module
