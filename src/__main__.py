#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from src import *
from src.lib.logger import setup_logger
from src.lib import config
from src.lib.handler import PluginHandler


def logs(config):
    level = config['app']['logger']['level']
    format = config['app']['logger']['format']
    return (level, format)


def app(config):
    return config['app']['name']


@click.command()
@click.option('--conf',
              required=False,
              default="./src/configuration.yml",
              help='Configuration file to use')
@click.pass_context
def main(ctx, conf):

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

    # construct dictionary of all args
    args_dict = ctx.params
    logger.debug("Args: {}".format(args_dict))

    # Construct PluginHandler instance
    # Process core plugins
    core_plugins_dir = configuration['app']['core']['directory']
    PluginHandler(logger, 'core', core_plugins_dir)

    # Process users plugins
    users_plugins_dir = configuration['app']['users']['directory']
    PluginHandler(logger, 'users', users_plugins_dir)


if __name__ == '__main__':
    main()
