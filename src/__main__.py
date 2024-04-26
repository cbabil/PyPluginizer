#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import shutil
import logging
import socket
from json import JSONEncoder
from codetiming import Timer
from src import *   # we need to review this. If commented then NameError: name '__modulename__' is not defined
from src.lib.logger import setup_logger
from src.lib import config
from src.lib.plugins import PluginManager
#from src.scanners.arp import arp_scan
#from src.netscanner.port import port_scan
#from src.netscanner.vendor import vendor_lookup
#from src.netscanner.ping import icmp_ping, arp_ping


def locate(cmd):
    '''Returns the path for a given binary

    Args:
        cmd (str): the binary

    Returns:
        path (str): path of the given binary if found
    '''
    path = shutil.which(cmd, path=None)
    if path:
        return path
    return None


def timers_clear():
    Timer.timers.clear()


def is_valid_ip(ip_address: str):
    """Checks if a given string is a valid IP address.

    Args:
        ip_address (str): The IP address to validate.

    Returns:
        bool: True if valid IP address, False otherwise.
    """
    try:
        socket.inet_aton(ip_address)
        return True
    except socket.error:
        return False


def print_version(ctx, config):
    """Prints the application version.

        Prints the configured application name and version 
        number to stdout and exits with status 0.
    """
    appversion = config['app']['version']
    appname = config['app']['name']
    print("\n{} {}\n".format(appname, appversion))
    ctx.exit(0)


def logs(config):
    level = config['app']['logger']['level']
    format = config['app']['logger']['format'] 
    return (level, format)


def plugins(config):
    directory = config['app']['plugins']['directory']
    return directory


def scanners(config):
    directory = config['app']['scanners']['directory']
    return directory


def app(config):
    name = config['app']['name']
    return name


@click.command()
@click.option('--ip', required=True, help='Ip address to scan')
@click.option('--inet', required=True, help='Interface to use')
@click.option('--conf',
              required=False,
              default="./src/configuration.yml",
              help='Configuration file to use'
)
#@click.option('--version',
#              is_flag=True,
#              callback=print_version,
#              is_eager=True,
#              expose_value=False,
#              help='Show the version and exit')
#@click.option('--connector', default='json', help='Output connector to use')
#@click.option('--arpscanTimeout', default=2, help='Arp Scan Timeout value')
#@click.option('--portscanTimeout', default=10, help='Port Scan Timeout value')
#@click.option('--pingTimeout', default=10, help='Ping Timeout value')
#@click.option('--version', is_flag=True, help='Show the version and exit')
#def main(ip, inet, version, connector, arpscantimeout, portscantimeout, pingtimeout):
@click.pass_context
def main(ctx, ip, inet, conf):
    '''Pi Detective network scanner'''

    # Parsing the configuration file
    configuration = config.yaml_parser(conf)

    # setup logging
    #   read the logger format from yml file
    #   if not defined default to something
    #   use the lib/log.py file for this
    (level, format) = logs(configuration)
    logger = setup_logger(level, format)
    logger.info("Running {} version {}".format(app(configuration), __version__))
    logger.info("Using configuration file: {}".format(conf))
    # Reset task timers
    timers_clear()

    # construct dictionary of all args
    args_dict = ctx.params
    logger.debug("Args: {}".format(args_dict))

    if ip:
        logger.info("Using ip: {}".format(ip))
    if inet:
        logger.info("Using interface: {}".format(inet))

    # Loading scanner plugins
    # in order based on the configuration
    scanners_dir = configuration['app']['scanners']['directory']

    # Create an instance of the PluginManager
    plugin_manager = PluginManager(logger)

    # Discover plugins in the "plugins" folder
    plugin_manager.discover(scanners_dir)

    # Load plugins
    plugin_manager.load()

    # Register the plugin with the PluginManager
    plugin_manager.register()

    # Get dependencies for each registered plugins
    plugin_manager.get_dependencies()

    # Resolve dependencies
    plugin_manager.resolve_dependencies()

    # Iterate over sorted plugins and execute them
    for plugin_name in plugin_manager.topological_sort():
        plugin_instance = plugin_manager.registered_plugins[plugin_name]
        plugin_instance.execute()

    logger.info("Scanning completed...")


if __name__ == '__main__':
    main()
