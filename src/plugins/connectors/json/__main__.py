import logging
from codetiming import Timer
import json


__version__ = "0.0.1"

logger = logging.getLogger(__name__)


@Timer(name="Import connector json",
       text="{name} finished in {:.4f} seconds...",
       logger=logging.info)
def main(data):
    """
    json connector
    """
    logger.info("Processing data...")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
