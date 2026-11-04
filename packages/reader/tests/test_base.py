from sidelight_reader.platform.base import TextSnapshot, WindowInfo


def test_window_info_is_immutable() -> None:
    w = WindowInfo(handle=1, title="Notes", process_name="notepad.exe")
    assert w.title == "Notes"


def test_snapshot_defaults() -> None:
    s = TextSnapshot(text="hello", source="accessibility")
    assert s.caret_offset is None
