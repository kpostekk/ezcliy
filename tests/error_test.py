from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

from ezcliy import *


def test_asking(capsys: CaptureFixture[str], monkeypatch: MonkeyPatch):
    monkeypatch.setattr('builtins.input', lambda _: 'que')

    class SpecialCommand(Command):
        flag_v = Flag('-v')
        pos_c = Positional('ccc', ask_if_missing='hmm?')
        allow_empty_calls = True

        def invoke(self):
            assert str(self.pos_c) == 'que'
            assert bool(self.flag_v) is True

    SpecialCommand().entry('-v')


def test_tmv(capsys: CaptureFixture[str]):
    class SpecialCommand(Command):
        pos = Positional('pos')
        restrict_to_positionals_only = True

    SpecialCommand().entry('a', 'b')
    capt = capsys.readouterr()
    assert 'error: TooManyValues' in capt.out


def test_optional():
    class SpecialCommand(Command):
        pos = Positional('pos', optional='hehehehe')
        allow_empty_calls = True

        def invoke(self):
            assert self.pos.value == 'hehehehe'

    SpecialCommand().entry()
