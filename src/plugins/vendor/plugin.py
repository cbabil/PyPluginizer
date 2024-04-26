import logging
from src.lib.plugins import PluginManager
from codetiming import Timer
from OuiLookup import OuiLookup

logger = logging.getLogger(__name__)


class Vendor(PluginManager):
    def __init__(self, args):
        super().__init__()
        self.ip = args.get("ip")
        self.add_dependency('arp')

    def execute(self):
        return self.lookup_vendor()

    def process_results(self, results):
        if results and 'vendor' in results:
            logger.info("Vendor found: %s", results['vendor'])
            return True
        else:
            logger.error("Vendor lookup failed.")
            return False

    @Timer(name="Vendor lookup",
           initial_text="Vendor lookup started...",
           text="{name} finished in {:.4f} seconds...",
           logger=logging.info)
    def lookup_vendor(self):
        results = {}
        try:
            if self.ip:
                lookup = OuiLookup()
                vendor = lookup.query(self.ip)
                if vendor:
                    vendor_name = str(list(vendor[0].values())[0])
                    logger.info("Vendor %s found for IP: %s", vendor_name, self.ip)
                    results['vendor'] = vendor_name
                else:
                    logger.info("Vendor not found for IP: %s", self.ip)
            else:
                logger.error("No IP address provided for vendor lookup.")
        except Exception as e:
            logger.exception("Error occurred during vendor lookup: %s", e)
        return results
