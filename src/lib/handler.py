# -*- coding: utf-8 -*-
from src.lib.hooks import HookManager
from src.lib.plugins import PluginManager


def HookHandler(logger, hook_dir=None):
    """
    Process hooks of the specified type.

    Args:
        logger: The logger object for logging messages.
        hook_dir (str, optional): The directory containing the hooks. If not provided, the current directory is used.
    """

    # Create an instance of the PluginManager
    hook_manager = HookManager(logger)
    # Discover hooks in the specified directory
    hook_manager.discover(hook_dir)
    return hook_manager.register() or None


def PluginHandler(logger, plugin_type, plugins_dir=None, hooks=None):
    """
    Process plugins of the specified type.

    Args:
        plugin_type (str): The type of plugins to process (e.g., 'core_plugins', 'scanners').
        logger: An instance of the logger to log messages.
        configuration (dict): The configuration settings for the application.

    Returns:
        bool: True if processing completes successfully, False otherwise.
    """
    try:
        logger.info("Processing %s plugins...", plugin_type)
        # Create an instance of the PluginManager
        plugin_manager = PluginManager(logger, hooks)

        # Discover plugins in the specified directory
        plugin_manager.discover(plugins_dir)

        # Load plugins
        plugin_manager.load()

        # Register plugins with the PluginManager
        plugin_manager.register()

        # Get dependencies for each registered plugin
        plugin_manager.get_dependencies()

        # Resolve dependencies
        plugin_manager.resolve_dependencies()

        # Iterate over sorted plugins and execute them
        for plugin_name in plugin_manager.topological_sort():
            plugin_instance = plugin_manager.registered_plugins[plugin_name]
            plugin_instance.execute()
            plugin_instance.process_results()

        logger.info("Processing %s plugins successfully...", plugin_type)
        return True  # Processing completes successfully
    except FileNotFoundError:
        logger.error("Directory '%s' not found...", plugins_dir)
        return False
    except KeyError:
        logger.exception("KeyError. Please check your configuration...")
        return False
    except Exception:
        logger.exception("An error occurred while processing %s plugins: ", plugin_type)
        return False
