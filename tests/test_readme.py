"""Run the documented quick start against the documented TOML contract."""

from pathlib import Path

import pytest


@pytest.mark.parametrize(
    ("rows", "expected"),
    [
        ("a@example.com,25,active\nb@example.com,30,pending\n", "Validation passed!"),
        ("a@example.com,25,active\na@example.com,30,pending\n", "fail: unique on email"),
        ("a@example.com,unknown,active\n", "skipped: range on age"),
    ],
)
def test_quick_start(tmp_path, monkeypatch, capsys, rows, expected):
    readme = (Path(__file__).parents[1] / "README.md").read_text(encoding="utf-8")
    example = readme.split("```python\n", 1)[1].split("```", 1)[0]
    contract = readme.split("```toml\n", 1)[1].split("```", 1)[0]
    (tmp_path / "contracts").mkdir()
    (tmp_path / "contracts" / "users.toml").write_text(contract, encoding="utf-8")
    (tmp_path / "users.csv").write_text("email,age,status\n" + rows, encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exec(compile(example, "README.md", "exec"), {})

    output = capsys.readouterr().out
    assert expected in output
    if expected != "Validation passed!":
        assert "Validation passed!" not in output
