# -*- coding: utf-8 -*-
class PluginError(Exception):
    """Base class for plugin-related errors."""

    pass


class PluginLoadError(PluginError):
    """Error raised when a plugin fails to load."""

    pass


class PluginRegistrationError(PluginError):
    """Error raised when a plugin fails to register."""

    pass


class PluginExecutionError(PluginError):
    """Error raised when a plugin execution fails."""

    pass
