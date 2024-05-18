# -*- coding: utf-8 -*-
import importlib.util
import os


class PluginManager:
    """A manager for handling plugins in an application."""

    def __init__(self, logger, hooks=None):
        """Initialize PluginManager."""
        self.hooks = hooks
        self.logger = logger
        self.plugins = {}
        self.discovered_plugins = {}
        self.loaded_plugins = {}
        self.registered_plugins = {}
        self.dependencies = {}
        self.resolved_plugins = set()
        self.sorted_plugins = []

    def discover(self, plugin_folder):
        """Discover plugins in the given folder."""
        self.logger.info('Discovering plugins in %s', plugin_folder)
        for module_path, _dirs, files in os.walk(plugin_folder):
            if 'IGNORE' in files:  # Check if the IGNORE file exists
                self.logger.info('Plugin ignored: %s', module_path)
                continue  # Skip this plugin if IGNORE file exists
            for file_name in files:
                if file_name.endswith('.py') and file_name != '__init__.py' and file_name == 'plugin.py':
                    relative_module_name = os.path.basename(module_path)  # Get the last directory name
                    self.logger.debug(
                        'Found plugin: %s (%s)',
                        relative_module_name,
                        module_path,
                    )
                    self.discovered_plugins[relative_module_name] = module_path

        self.logger.debug('Discovered plugins: %s', self.discovered_plugins)
        return self.discovered_plugins

    def load(self):
        """Load a plugin module."""
        try:
            for module_name, module_path in self.discovered_plugins.items():
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(module_path, '__init__.py'))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                # Log loading information
                self.logger.info(
                    'Loading plugin: %s version %s',
                    module.__name__,
                    module.__version__,
                )
                self.logger.debug('Module file path: %s', module.__file__)
                self.logger.debug('Module contents: %s', dir(module))
                self.loaded_plugins[module_name] = module
        except ImportError:
            self.logger.exception('Cannot import module from %s: ', module_path)
        except FileNotFoundError:
            self.logger.exception('Module file not found: %s')
        except AttributeError:
            self.logger.exception('Cannot load plugin: ')

        self.logger.debug('Loaded plugins: %s', self.loaded_plugins)
        return self.loaded_plugins

    def register(self, **kwargs):
        """Register all classes from plugins."""
        for module_name, module in self.loaded_plugins.items():
            try:
                module_path = getattr(module, '__file__', None)
                if module_path is None:
                    self.logger.error('Module file path not found for module: %s', module_name)
                    continue
                module_path = os.path.abspath(module_path)
                module_directory = os.path.dirname(module_path)
            except AttributeError:
                self.logger.exception('Invalid module object for module: %s', module_name)
                continue

            for name, obj in module.__dict__.items():
                if isinstance(obj, type):
                    plugin_instance = obj(self.logger, self.hooks, **kwargs)
                    self.registered_plugins[name] = plugin_instance
                    # this should be plugin_registered
                    # instead of plugins
                    self.plugins[name] = {
                        'module_name': module_name,
                        'module_path': module_path,
                        'module_directory': module_directory,
                        'module': module,
                        'instance': plugin_instance,
                    }
                    self.logger.info('Registered plugin: %s', name)

        self.logger.debug('Registered plugins: %s', self.registered_plugins)

        return self.registered_plugins

    def topological_sort(self):
        """
        Perform topological sorting on the plugins based on their dependencies.

        Returns:
            list: A list of plugin names sorted by their dependencies.
        """
        resolved_plugins = set()

        while len(self.sorted_plugins) < len(self.plugins):
            progress_made = False

            for plugin_name, _plugin_info in self.plugins.items():
                if plugin_name in resolved_plugins:
                    continue

                dependencies = self.dependencies.get(plugin_name, [])

                if all(dep in self.resolved_plugins for dep in dependencies):
                    self.sorted_plugins.append(plugin_name)
                    resolved_plugins.add(plugin_name)
                    progress_made = True

            if not progress_made:
                self.logger.error('Cycle detected in plugin dependencies.')
                break

        self.logger.info('Sorted plugins: %s', self.sorted_plugins)

        return self.sorted_plugins

    def resolve_dependencies(self):
        """Resolve dependencies for registered plugins."""

        # Track whether any progress has been made in resolving dependencies
        progress_made = True

        # Continue resolving dependencies until all plugins are resolved or no further progress can be made
        while self.resolved_plugins != set(self.plugins) and progress_made:
            progress_made = False

            for plugin_name, plugin_info in self.plugins.items():
                # Skip if plugin already resolved
                if plugin_name in self.resolved_plugins:
                    continue

                # Get dependencies for the current plugin
                dependencies = self.dependencies.get(plugin_name, [])

                # Filter out empty dependencies
                dependencies = [dep for dep in dependencies if dep]

                # Check if all dependencies are registered plugins
                if all(dep in self.plugins for dep in dependencies):
                    # Check if all dependencies are resolved
                    if all(dep in self.resolved_plugins for dep in dependencies):
                        # Instantiate the plugin if all dependencies are resolved
                        plugin_class = getattr(plugin_info['module'], plugin_name)
                        plugin_instance = plugin_class(self.logger)
                        plugin_info['instance'] = plugin_instance
                        self.resolved_plugins.add(plugin_name)
                        progress_made = True  # Progress has been made in resolving dependencies
                        self.logger.info('Resolved dependencies for plugin: %s', plugin_name)
                    else:
                        self.logger.debug(
                            'Plugin %s has unresolved dependencies: %s',
                            plugin_name,
                            dependencies,
                        )
                else:
                    self.logger.error(
                        'Plugin %s has unregistered dependencies: %s',
                        plugin_name,
                        dependencies,
                    )

        return self.resolved_plugins

    def get_dependencies(self):
        """Get dependencies for each registered plugin."""
        for plugin_name, plugin_info in self.plugins.items():
            plugin_directory = plugin_info['module_directory']
            dependency_file_path = os.path.join(plugin_directory, 'DEPENDENCY')
            dependencies = []

            self.logger.debug('Dependency file path: %s', dependency_file_path)
            if os.path.isfile(dependency_file_path):
                with open(dependency_file_path, 'r') as f:
                    content = f.read().strip()  # Read content and strip whitespace
                    if not content:  # Check if content is empty
                        self.logger.info('Dependencies for plugin %s: Not Found', plugin_name)
                    else:
                        dependencies = content.split('\n')
                        self.logger.info(
                            'Dependencies for plugin %s: %s',
                            plugin_name,
                            dependencies,
                        )
            else:
                self.logger.info('Dependencies for plugin %s: Not Found', plugin_name)

        self.dependencies[plugin_name] = dependencies

        return self.dependencies
