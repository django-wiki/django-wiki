from importlib import import_module

_cache = {}
_settings_forms = []
_markdown_extensions = []
_article_tabs = []
_sidebar = []
_html_whitelist = []
_html_attributes = {}


def register(PluginClass):
    """
    Register a plugin class. This function will call back your plugin's
    constructor.
    """
    if PluginClass in _cache:
        raise Exception("Plugin class already registered")
    plugin = PluginClass()
    _cache[PluginClass] = plugin

    settings_form = getattr(PluginClass, "settings_form", None)
    if settings_form:
        if isinstance(settings_form, str):
            klassname = settings_form.split(".")[-1]
            modulename = ".".join(settings_form.split(".")[:-1])
            form_module = import_module(modulename)
            settings_form = getattr(form_module, klassname)
        _settings_forms.append(settings_form)

    if getattr(PluginClass, "article_tab", None):
        _article_tabs.append(plugin)

    if getattr(PluginClass, "sidebar", None):
        _sidebar.append(plugin)

    _markdown_extensions.extend(getattr(PluginClass, "markdown_extensions", []))

    _html_whitelist.extend(getattr(PluginClass, "html_whitelist", []))

    _html_attributes.update(getattr(PluginClass, "html_attributes", dict()))


def get_plugins():
    """Get loaded plugins - do not call before all plugins are loaded."""
    return _cache


def get_markdown_extensions():
    """Get all markdown extension classes from plugins"""
    return _markdown_extensions


def get_article_tabs():
    """Get all article tab dictionaries from plugins"""
    return _article_tabs


def get_sidebar():
    """Returns plugin classes that should connect to the sidebar"""
    return _sidebar


def get_settings_forms():
    return _settings_forms


def get_html_whitelist():
    """Returns additional html tags that should be whitelisted"""
    return _html_whitelist


def get_html_attributes():
    """Returns additional html attributes that should be whitelisted"""
    return _html_attributes
