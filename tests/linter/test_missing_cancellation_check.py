import pytest

from .common import simple_ok_check, simple_nok_check, multiple_nok_check


# fmt: off
@pytest.mark.parametrize('code', [
"""
func foo(ct):
    await get_tree().process_frame
    if ct.is_cancelled():
        return
    print("ok")
""",
"""
func bar(cancellation_token):
    await some_coroutine()
    if cancellation_token.is_cancelled():
        return
""",
"""
func baz(ct):
    var x = 1
    await delayed_operation()
    if ct.is_cancelled():
        return
    await another_operation()
    if ct.is_cancelled():
        return
""",
"""
func with_return(ct):
    await operation()
    return
""",
"""
func last_statement(ct):
    await operation()
""",
"""
func with_if(ct):
    if ok:
        await operation()
        return
    await another_operation()
""",
])
def test_missing_cancellation_check_ok(code):
    simple_ok_check(code, disable=["unused-argument", "missing-cancellation-token-argument"])


@pytest.mark.parametrize('code,line', [
("""
func foo(ct):
    await get_tree().process_frame
    print("missing check")
""", 3),
("""
func chained_awaits(ct):
    await operation1()
    await operation2()
""", 3),
("""
func baz(ct):
    await operation1()
    if ct.is_cancelled():
        return
    await operation2()
    print("missing check after second await")
""", 6),
])
def test_missing_cancellation_check_nok(code, line):
    simple_nok_check(code, "missing-cancellation-check", line=line, disable=["unused-argument", "missing-cancellation-token-argument"])


@pytest.mark.parametrize('code,lines', [
("""
func apply(some_args) -> void:
	var animation_flow: AnimationFlow = _start_animation_flow(target, source_action)

	var applied_result: TimeoutOrSuccess = await animation_flow.applied.wait_with_timeout(10, ct)
	applied_result.push_error_if_timeout(_applied_error_message_if_timeout(source_action))

	await _apply_effect_async(target, source_action, history, ct)
	if ct.is_cancelled():
		_playing_animation_effect = CompletedActionEffectAnimation.new()
		return

	var ended_wait_result: TimeoutOrSuccess = await animation_flow.ended.wait_with_timeout(10, ct)
	ended_wait_result.push_error_if_timeout(_ended_error_if_timeout_message(source_action))

	_playing_animation_effect = CompletedActionEffectAnimation.new()
""", [5, 13]),
])
def test_missing_cancellation_check_multiple_nok(code, lines):
    multiple_nok_check(code, "missing-cancellation-check", lines=lines, disable=["unused-argument", "missing-cancellation-token-argument"])


# Tests for gdlint ignore comments
@pytest.mark.parametrize('code', [
"""
func test1(ct):
    await method1(ct)  # gdlint: ignore=missing-cancellation-check
""",
"""
func test2(ct):
    # gdlint: ignore=missing-cancellation-check
    await method2(ct)
""",
"""
# gdlint: disable=missing-cancellation-check
func test3(ct):
    await method3(ct)

func test4(ct):
    await method4(ct)
# gdlint: enable=missing-cancellation-check
""",
])
def test_missing_cancellation_check_with_ignore_comments(code):
    simple_ok_check(code, disable=["unused-argument", "missing-cancellation-token-argument"])