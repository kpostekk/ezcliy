from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from ezcliy import *
from ezcliy.exceptions import UnexceptedNumberOfValues


def test_asking(capsys: CaptureFixture[str], monkeypatch: MonkeyPatch):
    monkeypatch.setattr('builtins.input', lambda _: 'que')

    class SpecialCommand(Command):
        flag_v = Flag('-v')
        pos_c = Positional('ccc', ask_if_missing='hmm?')
        none_args_will_not_trigger_help = True

        def invoke(self):
            assert str(self.pos_c) == 'que'
            assert bool(self.flag_v) is True

    SpecialCommand().entry('-v')


def test_tmv(capsys: CaptureFixture[str]):
    class SpecialCommand(Command):
        pos = Positional('pos')
        require_all_defined_positionals = True

    try:
        SpecialCommand().entry('a', 'b')
        errored = False
    except UnexceptedNumberOfValues as err:
        errored = True

    assert errored


def test_optional():
    class SpecialCommand(Command):
        pos = Positional('pos', optional='hehehehe')
        none_args_will_not_trigger_help = True

        def invoke(self):
            assert self.pos.value == 'hehehehe'

    SpecialCommand().entry()
