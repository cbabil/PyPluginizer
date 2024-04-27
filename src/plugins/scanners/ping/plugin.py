import logging
from codetiming import Timer
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import srp, sr, Ether, ARP, IP, ICMP
from scapy.error import Scapy_Exception


logger = logging.getLogger(__name__)


class Ping:
    def __init__(self):
        pass

    def execute(self):
        logger.info("Executing MyPlugin")

    def process_results(self, results):
        logger.info("Processing results in MyPlugin")

    def hook_method(self, *args, **kwargs):
        logger.info("Hook method called in MyPlugin")


@Timer(name="Arp Ping",
       initial_text="Arp ping started...",
       text="{name} finished in {:.4f} seconds...",
       logger=logging.info)
def arp_ping(host: str, timeout: int):
    '''ARP Ping

    Args:
        host (str): host
        timeout (int): timeout
    '''
    try:
        # The fastest way to discover hosts on a local ethernet network is to use the ARP Ping method:
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=host), timeout=timeout, verbose=False)

        # Answers can be reviewed with the following command:
        logger.info(ans.summary(lambda p: p[1].sprintf("IP: %ARP.psrc%   MAC: %Ether.src%")))
    except IndexError:
        logger.err("No device found: {}".format(host))
    return


@Timer(name="Icpm Ping",
       initial_text="Icmp ping started...",
       text="{name} finished in {:.4f} seconds...",
       logger=logging.info)
def icmp_ping(host: str, timeout: int):
    '''ICMP Ping

    Args:
        host (str): host
        timeout (int): timeout
    '''

    # Classical ICMP Ping can be emulated using the following command:
    ans, unans = sr(IP(dst=host) / ICMP())

    # Information on live hosts can be collected with the following request:
    ans.summary(lambda p: p[1].sprintf("%IP.src% is alive"))


@Timer(name="Tcp Ping",
       initial_text="Tcp ping started...",
       text="{name} finished in {:.4f} seconds...",
       logger=logging.info)
def tcp_ping(host):
    return


@Timer(name="Udp Ping",
       initial_text="Udp ping started...",
       text="{name} finished in {:.4f} seconds...",
       logger=logging.info)
def udp_ping(host):
    return


def ping_host(interface, ip, timeout):
    client_dict = {}
    res = arp_ping(ip, timeout)
    logger.info(res)

    return client_dict


