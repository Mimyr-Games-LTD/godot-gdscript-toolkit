import pytest

from gdtoolkit.linter import lint_code, DEFAULT_CONFIG


def _config_with_plugin(plugin_path):
    config = DEFAULT_CONFIG.copy()
    config.update({"plugins": [plugin_path]})
    return config


def test_plugin_loading_with_valid_module():
    code = "func foo():\n    pass\n"
    config = _config_with_plugin("gdtoolkit.linter.basic_checks")
    result = lint_code(code, config)
    assert isinstance(result, list)


def test_plugin_loading_with_missing_module():
    code = "func foo():\n    pass\n"
    config = _config_with_plugin("nonexistent_module_xyz")
    result = lint_code(code, config)
    assert isinstance(result, list)


def test_plugin_loading_with_empty_plugins():
    code = "func foo():\n    pass\n"
    config = DEFAULT_CONFIG.copy()
    config.update({"plugins": []})
    result = lint_code(code, config)
    assert isinstance(result, list)


def test_plugin_loading_with_no_plugins_key():
    code = "func foo():\n    pass\n"
    result = lint_code(code, DEFAULT_CONFIG)
    assert isinstance(result, list)
