import pytest

from .common import simple_ok_check, simple_nok_check


# fmt: off
@pytest.mark.parametrize('code', [
"""
func process_async():
    await operation()
""",
"""
func load_data_async(ct):
    await fetch_data()
    if ct.is_cancelled():
        return
""",
"""
func _internal_method_async():
    await something()
""",
"""
func no_await():
    print("no await here")
""",
])
def test_async_function_name_ok(code):
    simple_ok_check(code, disable=["unused-argument", "missing-ct-check", "missing-ct-arg", "missing-ct-param"])


@pytest.mark.parametrize('code,line', [
("""
func process():
    await operation()
""", 2),
("""
func load_data(ct):
    await fetch_data()
""", 2),
("""
func _internal_method():
    await something()
""", 2),
])
def test_async_function_name_nok(code, line):
    simple_nok_check(code, "async-function-name", line=line, disable=["unused-argument", "missing-ct-check", "missing-ct-arg", "missing-ct-param"])
