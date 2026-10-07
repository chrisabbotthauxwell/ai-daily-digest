from ingest.main import main


def test_main_exits_cleanly() -> None:
    assert main() == 0
