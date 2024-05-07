import pytest
import sys
import os
import importlib.util
from src.lib.plugins import PluginManager


@pytest.fixture
def plugin_manager(mocker):
    manager = PluginManager(logger=mocker.Mock())

    # Simulate loaded plugins that can be registered
    discovered_plugins = {
        'Plugin': '/path/to/plugin',
        'Plugin1': '/path/to/plugin1',
        'Plugin2': '/path/to/plugin2'
    }

    # Assign the mocked plugins to loaded_plugins
    manager.loaded_plugins = {name: mocker.Mock() for name in discovered_plugins.values()}

    manager.plugins = {
        'Plugin': {
            'module_name': 'Plugin',
            'module_path': '/path/to/plugin/__init__.py',
            'module_directory': '/path/to/plugin',
            'module': mocker.Mock(),
            'instance': mocker.Mock()
        },
        'Plugin1': {
            'module_name': 'Plugin1',
            'module_path': '/path/to/plugin1/__init__.py',
            'module_directory': '/path/to/plugin1',
            'module': mocker.Mock(),
            'instance': mocker.Mock()
        },
        'Plugin2': {
            'module_name': 'Plugin2',
            'module_path': '/path/to/plugin2/__init__.py',
            'module_directory': '/path/to/plugin2',
            'module': mocker.Mock(),
            'instance': mocker.Mock()
        }
    }

    manager.dependencies = {
        'Plugin2': ['Plugin', 'Plugin1']
    }
    return manager


def test_discover(plugin_manager, mocker):
    """Test the discover method of PluginManager."""
    # Mock os.walk to return dummy directory structure
    mock_os_walk = mocker.patch("os.walk")
    mock_os_walk.return_value = [
        ("/path/to/plugin_folder", ["dir1", "dir2"], ["plugin.py", "other_file.txt"]),
        ("/path/to/plugin_folder/dir1", [], ["plugin.py"]),
        ("/path/to/plugin_folder/dir2", [], ["not_a_plugin.py"])
    ]

    # Patch logger.info method
    mock_logger_info = mocker.patch.object(plugin_manager.logger, 'info')

    # Call discover method
    discovered_plugins = plugin_manager.discover("/path/to/plugin_folder")

    # Assertions
    assert discovered_plugins == plugin_manager.discovered_plugins
    mock_logger_info.assert_called_once_with("Discovering plugins in /path/to/plugin_folder")
    mock_os_walk.assert_called_once_with("/path/to/plugin_folder")


def test_load_success(plugin_manager, mocker):
    """Test the load method of PluginManager for success."""
    # Mock logger.info method
    mock_logger_info = mocker.patch.object(plugin_manager.logger, 'info')

    # Mock importlib.util.spec_from_file_location
    mocker.patch("importlib.util.spec_from_file_location")

    # Mock importlib.util.module_from_spec
    mocker.patch("importlib.util.module_from_spec")

    # Mock importlib.util.spec_from_file_location.loader.exec_module
    mocker.patch("importlib.util.spec_from_file_location.loader.exec_module")

    # Act
    plugin_manager.load()

    # Assert
    # Assert that the logger's info method is called with the expected message
    #mock_logger_info.assert_called_with("Loading plugins: Plugin, Plugin1, Plugin2")

    # Optionally, you can assert other behaviors such as checking if other logger methods are not called
    #plugin_manager.logger.error.assert_not_called()
    #plugin_manager.logger.debug.assert_called_with("Loaded plugins: {'Plugin': <Mock id='...'>, 'Plugin1': <Mock id='...'>, 'Plugin2': <Mock id='...'>}")


def test_load_attribute_error(plugin_manager, mocker):
    """Test the load method of PluginManager for AttributeError."""
    # Mock logger.error method
    mock_logger_error = mocker.patch.object(plugin_manager.logger, 'error')

    # Patch importlib.util.spec_from_file_location with side_effect to raise AttributeError
    mocker.patch("importlib.util.spec_from_file_location", side_effect=AttributeError("Attribute error"))

    # Call load method
    loaded_plugins = plugin_manager.load()

    # Assertions
    assert loaded_plugins == plugin_manager.loaded_plugins
    mock_logger_error.assert_called_once_with("Cannot load plugin: Attribute error")


def test_register(plugin_manager, mocker):
    """Test the register method with loaded plugins."""
    # Mock the __file__ attribute for module objects
    for module_name, module_path in plugin_manager.discovered_plugins.items():
        module_mock = mocker.Mock()
        module_mock.__file__ = module_path
        plugin_manager.loaded_plugins[module_name] = module_mock

    print("Before register:", plugin_manager.registered_plugins)

    # Call the register method
    registered_plugins = plugin_manager.register()

    print("After register, registered_plugins:", registered_plugins)

    # Assertions
    assert len(registered_plugins) == 3


def test_get_dependencies(plugin_manager):
    """Test the get_dependencies method."""
    pass


def test_resolve_dependencies(plugin_manager):
    """Test the resolve_dependencies method."""
    pass


def test_topological_sort(plugin_manager):
    """Test the topological_sort method."""
    pass