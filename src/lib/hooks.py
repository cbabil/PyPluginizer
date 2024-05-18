# -*- coding: utf-8 -*-
import importlib.util
import os


class HookManager:
    """
    A class for managing hooks and triggering associated functions.
    """

    def __init__(self, logger):
        """
        Initialize the Hook instance.

        Args:
            logger (Logger): The logger to use for logging.
        """
        self.logger = logger
        self.discovered_hooks = {}
        self.registered_hooks = {}

    def discover(self, hook_folder):
        """
        Discover hooks in the given folder.

        Args:
            hook_folder (str): The folder to discover hooks in.

        Returns:
            dict: A dictionary of discovered hooks.
        """
        if hook_folder is None:
            self.logger.info("No hooks to discover.")
            return None
        self.logger.info("Discovering hooks in %s...", hook_folder)
        for module_path, _dirs, files in os.walk(hook_folder):
            for file_name in files:
                if file_name.endswith(".py") and file_name != "__init__.py":
                    relative_module_name = os.path.basename(module_path)
                    self.logger.debug("Found hook: %s (%s)", relative_module_name, module_path)
                    self.discovered_hooks[relative_module_name] = module_path

        self.logger.debug("Discovered hooks: %s", self.discovered_hooks)
        return self.discovered_hooks

    def register(self):
        """
        Register function to be called when the specified hook is triggered.
        """
        for hook, hook_path in self.discovered_hooks.items():
            try:
                if not os.path.exists(hook_path):
                    self.logger.error(f"Failed to import hook {hook}: {hook_path} path not found")
                    continue
                self.logger.debug(f"Importing hook {hook}: {hook_path}")
                spec = importlib.util.spec_from_file_location(hook, os.path.join(hook_path, "__init__.py"))
                if spec is None:
                    self.logger.error(f"Failed to import hook {hook}: {hook_path} not found")
                    continue
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                # Log loading information
                self.logger.info(
                    "Loading hook: %s version %s",
                    module.__name__,
                    module.__version__,
                )
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if type(attr) is type:
                        self.logger.info("Registering class %s to hook %s", attr_name, hook)
                        hook_instance = attr(self.logger)
                        self.registered_hooks[hook] = hook_instance

            except ImportError as err:
                self.logger.error("Failed to import hook %s: %s", hook, err)
            except AttributeError as err:
                self.logger.error("Failed to create spec for %s: %s", hook_path, err)

        self.logger.debug("Registered hooks: %s", self.registered_hooks)

        return self.registered_hooks
