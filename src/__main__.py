#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import click

from src import __version__
from src.lib import config
from src.lib.handler import HookHandler, PluginHandler
from src.lib.logger import setup_logger


def logs(configuration):
    """Return the logger format and level from the configuration file"""
    loglevel = configuration['app']['logger']['level']
    logformat = configuration['app']['logger']['format']
    return (loglevel, logformat)


def app(configuration):
    """Return the application name from the configuration file"""
    return configuration['app']['name']


@click.command()
@click.option(
    '--conf',
    required=False,
    default='./src/configuration.yml',
    help='Configuration file to use',
)
@click.pass_context
def main(ctx, conf):
    """Main entry point for the application."""
    # Parsing the configuration file
    configuration = config.yaml_parser(conf)

    # setup logging
    #   read the logger format from yml file
    #   if not defined default to something
    #   use the lib/log.py file for this
    (loglevel, logformat) = logs(configuration)
    logger = setup_logger(loglevel, logformat)
    logger.info('Running %s version %s', app(configuration), __version__)
    logger.info('Using configuration file: %s', conf)

    # construct dictionary of all args
    args_dict = ctx.params
    logger.debug('Args: %s', args_dict)

    # Process hooks
    hooks_dir = configuration['app']['hooks']['directory']
    hooks = HookHandler(logger, hooks_dir)

    plugins = {
        'core': configuration['app']['core']['directory'],
        'users': configuration['app']['users']['directory'],
    }

    # Processing core and users plugins
    for type, path in plugins.items():
        PluginHandler(logger, type, path, hooks)


if __name__ == '__main__':
    main()
