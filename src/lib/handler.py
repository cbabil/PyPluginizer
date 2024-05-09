# -*- coding: utf-8 -*-
from src.lib.plugins import PluginManager


def PluginHandler(logger, plugin_type, plugins_dir=None):
    """
    Process plugins of the specified type.

    Args:
        plugin_type (str): The type of plugins to process (e.g., 'core_plugins', 'scanners').
        logger: An instance of the logger to log messages.
        configuration (dict): The configuration settings for the application.

    Returns:
        bool: True if processing completes successfully, False otherwise.
    """
    logger.info('Processing %s plugins...', plugin_type)
    try:
        # Create an instance of the PluginManager
        plugin_manager = PluginManager(logger)

        # Discover plugins in the specified directory
        plugin_manager.discover(plugins_dir)

        # Load plugins
        plugin_manager.load()

        # Register plugins with the PluginManager
        plugin_manager.register(logger=logger)

        # Get dependencies for each registered plugin
        plugin_manager.get_dependencies()

        # Resolve dependencies
        plugin_manager.resolve_dependencies()

        # Iterate over sorted plugins and execute them
        for plugin_name in plugin_manager.topological_sort():
            plugin_instance = plugin_manager.registered_plugins[plugin_name]
            plugin_instance.execute()
            plugin_instance.process_results()

        logger.info('Processing %s plugins sucessfully...', plugin_type)
        return True  # Processing completes successfully
    except FileNotFoundError:
        logger.error("Directory '%s' not found...", plugins_dir)
        return False
    except KeyError:
        logger.exception('KeyError. Please check your configuration...')
        return False
    except Exception:
        logger.exception('An error occurred while processing %s plugins: ', plugin_type)
        return False
