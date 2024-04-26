from src.lib.plugins import PluginManager
import logging
from codetiming import Timer
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import ARP, Ether, srp
from scapy.error import Scapy_Exception


logger = logging.getLogger(__name__)


class Arp(PluginManager):
    def __init__(self, args):
        # Call the parent class's __init__ method
        super().__init__()

        # Initialize attributes specific to the Arp plugin
        self.interface = args.get("interface")
        self.ip = args.get("ip")
        self.timeout = args.get("timeout")
        

    def execute(self):
        return self.arp_scan()

    def process_results(self, results):
        if results:
            # Process results here
            return True  # Return True for success
        else:
            return False  # Return False for failure

    @Timer(name="Arp scan",
           initial_text="Arp scan started...",
           text="{name} finished in {:.4f} seconds...",
           logger=logging.info)
    def arp_scan(self):
        arp_request = ARP(pdst=self.ip)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        client_dict = {}
        try:
            answered_list = srp(arp_request_broadcast,
                                timeout=self.timeout,
                                iface=self.interface,
                                inter=0.1,
                                verbose=False)[0]
            for element in answered_list:
                ipaddr = element[1].psrc
                mac = element[1].hwsrc
                client_dict[mac] = {"ip": ipaddr}
        except Scapy_Exception as err:
            logger.exception(err)

        return client_dict
