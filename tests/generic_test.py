import json

import pytest
from _pytest.capture import CaptureFixture

from ezcliy import Command, Flag, Positional, KeyVal


def test_flags(capsys: CaptureFixture[str]):
    class TestingCommand(Command):
        a = Flag('-a', '--aaa')
        v = Flag('-v')

        def invoke(self):
            if self.a:
                print(len(self.values), end='')

    TestingCommand().entry('-a', '--aaa', '-v', '-t')
    capt = capsys.readouterr()
    assert capt.out == '0'


def test_keyvals(capsys: CaptureFixture[str]):
    class TestingCommand(Command):
        a = KeyVal('-a')
        b = KeyVal('-b')

        def invoke(self):
            print(self.a, end='')

    TestingCommand().entry('-a', '2137', '-a', '1337', '-b')
    capt = capsys.readouterr()
    assert capt.out == '2137'


def test_simple_subcmd(capsys: CaptureFixture[str]):
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
                print(
                    json.dumps(
                        [
                            self.inner_pos.value,
                            self.root_flag.value,
                            self.inner_flag.value,
                            self.inner_kv.value
                        ]
                    ), end=''
                )

    SpecialCommand().entry('sub', 'pytest is fun', '-o', '-i', '--ik', '420')
    capt = capsys.readouterr()
    assert capt.out == json.dumps(['pytest is fun', True, True, '420'])


def test_help_renderer():
    class SpecialCommand(Command):
        flag_a = Flag('-a')
        kv_b = KeyVal('-b')
        pos_c = Positional('ccc')

        def invoke(self):
            print('AAAAAAAAA')

        class OtherCommand(Command):
            name = 'oocc'

    help_str = SpecialCommand()._help.render_help(SpecialCommand())
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
