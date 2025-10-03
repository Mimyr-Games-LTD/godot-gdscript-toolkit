import pytest

from .common import simple_ok_check, simple_nok_check


# fmt: off
@pytest.mark.parametrize('code', [
"""
func process_async(ct: CancellationToken):
    await operation(ct)
    if ct.is_cancelled():
        return
""",
"""
func load_data_async(ct):
    await fetch_data(ct)
""",
"""
func no_await():
    print("no await here")
""",
])
def test_missing_cancellation_token_parameter_ok(code):
    simple_ok_check(code, disable=["unused-argument", "missing-cancellation-check", "missing-ct-arg"])


@pytest.mark.parametrize('code,line', [
("""
func process_async():
    await operation()
""", 2),
("""
func _apply(effect_target: Target, _source_action: BattlegroundAction, _history: ActionExecutionHistory) -> void:
	await effect_target.bg_targets().each_position_async(_summon_async_callable)

func _summon_async_callable(position: Vector2i, ct: CancellationToken) -> void:
    ### some code
    await unit.view().components().defenses_animations().play_spawn_animation_async(ct)
	if ct.is_cancelled():
		return
	await unit.activation_strategy().activate_on_phase_async(RunStateMachine.CombatPhase.ENEMY_DECLARE_ACTION, [], ct)
""", 2),
])
def test_missing_cancellation_token_parameter_nok(code, line):
    simple_nok_check(code, "missing-ct-param", line=line, disable=["unused-argument", "missing-cancellation-check", "async-function-name", "max-line-length", "trailing-whitespace", "missing-ct-arg"])
