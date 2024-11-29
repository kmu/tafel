import pytest
from tafel.app.cli import main


def test_main(capsys: pytest.CaptureFixture):
    main()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"
