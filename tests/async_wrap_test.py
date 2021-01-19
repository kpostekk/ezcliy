from _pytest.capture import CaptureFixture

from ezcliy import Command, KeyVal


def test_coro(capsys: CaptureFixture[str]):
    from asyncio import sleep

    class TestingCommand(Command):
        wait = KeyVal('-w', default=60)

        async def invoke(self):
            await sleep(float(self.wait.value))
            print(self.wait.value)

    TestingCommand().entry('-w', '0.1')
    capt = capsys.readouterr()
    assert capt.out == '0.1\n'
