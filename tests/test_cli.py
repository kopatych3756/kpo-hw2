from pos.infrastructure.container import Container
from pos.result.cli import ConsoleUI


def test_cli_complete_scenario(monkeypatch, capsys):
    values = iter([
        "1", "1", "Иван",
        "5", "1", "Домашка", "10", "2",
        "7", "1", "1", "8",
        "11", "1",
        "0"
    ])
    monkeypatch.setattr("builtins.input",lambda _: next(values))
    app = Container().create_app()
    ConsoleUI(app).run()
    output = capsys.readouterr().out
    assert "Итог для Иван: 80.0%" in output

def test_cli_shows_domain_error(monkeypatch, capsys):
    values = iter([
        "1", "1", "Иван",
        "5", "1", "Домашка", "10", "2",
        "7", "1", "1", "15",
        "0"
    ])
    monkeypatch.setattr("builtins.input",lambda _: next(values))
    app = Container().create_app()
    ConsoleUI(app).run()
    output = capsys.readouterr().out
    assert "Оценка превышает максимальный балл" in output

