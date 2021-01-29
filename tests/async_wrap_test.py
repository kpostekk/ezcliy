from _pytest.capture import CaptureFixture

from ezcliy import Command, KeyVal


def test_coro(capsys: CaptureFixture[str]):
    from asyncio import sleep

    class TestingCommand(Command):
        wait = KeyVal('-w', default=60)

        async def invoke(self):
            await sleep(float(self.wait))
            print(self.wait)

    TestingCommand().entry('-w', '0.1')
    capt = capsys.readouterr()
    assert capt.out == '0.1\n'


def test_subcoro(capsys: CaptureFixture[str]):
    from asyncio import sleep

    class TestingCommand(Command):
        async def invoke(self):
            await sleep(0.1)
            print(0)

        class TestingSubCommand(Command):
            name = 'tsc'
            allow_empty_calls = True

            async def invoke(self):
                await sleep(0.2)
                print(1)

    TestingCommand().entry('tsc')
    capt = capsys.readouterr()
    assert capt.out == '0\n1\n'
