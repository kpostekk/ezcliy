import json

from _pytest.capture import CaptureFixture

from ezcliy import Command, Flag, Positional, KeyVal


def test_flags(capsys: CaptureFixture[str]):
    class TestingCommand(Command):
        a = Flag('-a', '--aaa')
        v = Flag('-v')

        def invoke(self):
            if self.a:
                print(len(self.values), end='')

    expected = '0'
    TestingCommand().entry('-a', '--aaa', '-v', '-t')
    capt = capsys.readouterr()
    assert capt.out == expected


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
    expected = ['pytest is fun', True, True, '420']

    SpecialCommand().entry('sub', 'pytest is fun', '-o', '-i', '--ik', '420')
    capt = capsys.readouterr()
    assert capt.out == json.dumps(expected)
