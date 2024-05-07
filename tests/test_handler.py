import pytest
from src.lib.plugins import PluginManager
from src.lib.handler import PluginHandler


@pytest.fixture
def logger(mocker):
    return mocker.Mock()


@pytest.fixture
def plugin_manager(mocker):
    manager = PluginManager(logger=mocker.Mock())
    return manager


def test_plugin_handler(logger, plugin_manager, mocker):
    # Mocking PluginManager methods
    mocker.patch.object(plugin_manager, "discover", return_value=None)
    mocker.patch.object(plugin_manager, "load", return_value=None)
    mocker.patch.object(plugin_manager, "register", return_value=None)
    mocker.patch.object(plugin_manager, "get_dependencies", return_value=None)
    mocker.patch.object(plugin_manager, "resolve_dependencies", return_value=None)
    mocker.patch.object(plugin_manager, "topological_sort", return_value=["plugin1", "plugin2"])
    plugin_manager.registered_plugins = {
        "plugin1": mocker.Mock(),
        "plugin2": mocker.Mock()
    }

    # Fake plugins_dir
    plugins_dir = "/fake/plugins/directory"

    # Calling PluginHandler
    PluginHandler(logger, "core_plugins", plugins_dir)

    # Asserting that PluginManager methods were called with the correct arguments
    plugin_manager.discover.assert_called_once_with(plugins_dir)
    plugin_manager.load.assert_called_once()
    plugin_manager.register.assert_called_once()
    plugin_manager.get_dependencies.assert_called_once()
    plugin_manager.resolve_dependencies.assert_called_once()
    plugin_manager.topological_sort.assert_called_once()

    # Expected logger calls
    expected_logger_calls = [
        mocker.call("Processing core_plugins plugins..."),
        mocker.call("Processing core_plugins plugins successfully...")
    ]
    logger.info.assert_has_calls(expected_logger_calls, any_order=False)



def test_plugin_handler_directory_not_found(logger, plugin_manager, mocker):
    mocker.patch("src.lib.plugins.PluginManager", return_value=plugin_manager)
    plugins_dir = "/path/to/nonexistent/plugins"

    # Simulating FileNotFoundError
    plugin_manager.discover.side_effect = FileNotFoundError

    assert not PluginHandler(logger, "core_plugins", plugins_dir)

    logger.error.assert_called_with("Directory '/path/to/nonexistent/plugins' not found...")
