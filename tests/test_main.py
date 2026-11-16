from pos.main import main


def test_main_starts_and_exits(monkeypatch, tmp_path, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("builtins.input", lambda _: "0")
    main()
    output = capsys.readouterr().out
    assert "ПОС" in output
