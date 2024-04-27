import logging
import random
from codetiming import Timer
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP, sr, sr1, TCP

logger = logging.getLogger(__name__)


@Timer(name="Port scan",
       initial_text="Port scan started...",
       text="{name} finished in {:.4f} seconds...",
       logger=logging.info)
def port_scan(host, timeout):
    # Ports that will be scanned:
    # 21 - FTP
    # 22 - SSH
    # 23 - Telnet
    # 25 - SMTP
    # 53 - DNS
    # 80 - HTTP
    # 110 - POP3
    # 135 - Windows RPC
    # 137 - Windows NetBIOS over TCP
    # 138 - Windows NetBIOS over TCP
    # 139 - Windows NetBIOS over TCP
    # 443 - HTTPS
    # 1433 - Microsoft SQL Server
    # 1434 - Microsoft SQL Server
    # 8080 - HTTP Alternative
    PortRange = [21, 22, 23, 25, 53, 80, 110, 135, 137, 138, 139, 443, 1433, 1434, 8080]
    p_open = []
    p_closed = []
    p_filtered = []
    p_opencount = 0
    p_closedcount = 0
    p_filteredcount = 0
    logger.info("Port Range: %s", PortRange)
    for destPort in PortRange:
        # Source port is randomized using the random
        # module from port 1025 to 65334.
        srcport = random.randint(1025, 65534)
        tcp_connect_scan_resp = sr1(IP(dst=host) / TCP(sport=srcport,
                                    dport=destPort,
                                    flags="S"),
                                    timeout=timeout,
                                    verbose=0)
        # If there is not answer from the port scanned
        # the program will print the port is filtered
        if tcp_connect_scan_resp is None:
            p_filtered.append(destPort)
            p_filteredcount += 1
        elif tcp_connect_scan_resp.haslayer(TCP):
            # If the port scanned give answers with a SYN ACK
            # the program will print the port is open
            if tcp_connect_scan_resp.getlayer(TCP).flags == 0x12:
                send_rst = sr(IP(dst=host) / TCP(sport=srcport, dport=destPort, flags="AR"), timeout=timeout, verbose=0)
                p_open.append(destPort)
                p_opencount += 1
            # If the port gives an answer but resets
            # the connection the program will print
            # the port is closed.
            elif tcp_connect_scan_resp.getlayer(TCP).flags == 0x14:
                p_closed.append(destPort)
                p_closedcount += 1

    return dict(open=p_open,
                close=p_closed,
                filtered=p_filtered,
                totalopen=p_opencount,
                totalclose=p_closedcount,
                totalfiltered=p_filteredcount,
                total=p_opencount + p_closedcount + p_filteredcount)
