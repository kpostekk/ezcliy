import pytest
from _pytest.capture import CaptureFixture

from ezcliy import Command, Flag, Positional, KeyVal


def test_flags():
    class TestingCommand(Command):
        a = Flag('-a', '--aaa')
        v = Flag('-v')
        u = Flag('-u')

        def invoke(self):
            assert bool(self.a) is True
            assert bool(self.v) is True
            assert bool(self.u) is False

    TestingCommand().entry('-a', '--aaa', '-v', '-t')


def test_keyvals():
    class TestingCommand(Command):
        a = KeyVal('-a')
        b = KeyVal('-b')

        def invoke(self):
            assert int(self.a) == 2137
            assert self.a.values == ['2137', '1337']
            assert self.b.value is None

    TestingCommand().entry('-a', '2137', '-a', '1337', '-b')


def test_simple_subcmd():
    class SpecialCommand(Command):
        root_flag = Flag('-o')

        class Subc(Command):
            name = 'sub'
            inner_pos = Positional('inner pos')
            inner_kv = KeyVal('--ik', default='69')
            root_flag: Flag
            inner_flag = Flag('-i')
            restrict_to_positionals_only = True

            def invoke(self):
                assert bool(self.root_flag) is True
                assert bool(self.inner_flag) is True
                assert str(self.inner_pos) == 'pytest is fun'
                assert int(self.inner_kv) == 420

        def invoke(self):
            assert bool(self.root_flag) is True

    SpecialCommand().entry('sub', 'pytest is fun', '-o', '-i', '--ik', '420')


def test_help_renderer():
    class SpecialCommand(Command):
        flag_a = Flag('-a')
        kv_b = KeyVal('-b')
        pos_c = Positional('ccc')

        def invoke(self):
            ...

        class OtherCommand(Command):
            name = 'oocc'

    help_str = SpecialCommand()._helpman.render_help(SpecialCommand())
    assert '-a' in help_str
    assert '-b' in help_str
    assert 'ccc' in help_str


def test_help_flag(capsys: CaptureFixture[str]):
    class SpecialCommand(Command):
        flag_a = Flag('-a', '--aaa')
        flag_a.description = 'I like jazz'

    with pytest.raises(SystemExit) as wrapped_e:
        SpecialCommand().entry(*['--help'])
    capt = capsys.readouterr()
    assert wrapped_e.type == SystemExit
    assert '--help' in capt.out
    assert '--aaa' in capt.out
    assert 'I like jazz' in capt.out
