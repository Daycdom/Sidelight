from sidelight_common.paths import config_dir, data_dir


def test_dirs_are_named_for_the_app() -> None:
    assert "Sidelight" in str(config_dir())
    assert "Sidelight" in str(data_dir())
