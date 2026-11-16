import csv
from pos.infrastructure.container import Container


def test_export_results(tmp_path):
    app = Container().create_app()
    app.add_student(1, "Иван")
    app.add_student(2, "Мария")
    app.add_criterion(1, "Домашка", 10, 2)
    app.add_evaluation(1, 1, 8)
    filename = tmp_path / "results.csv"
    app.export_results(filename)
    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file, delimiter=";"))
    assert len(rows) == 2
    assert rows[0]["student_name"] == "Иван"
    assert rows[0]["final_score"] == "80.0"
    assert rows[1]["student_name"] == "Мария"
    assert rows[1]["final_score"] == "0.0"

def test_export_updated_score(tmp_path):
    app = Container().create_app()
    app.add_student(1, "Иван")
    app.add_criterion(1, "Домашка", 10, 2)
    app.add_evaluation(1, 1, 8)
    app.update_evaluation(1, 1, 9)
    filename = tmp_path / "results.csv"
    app.export_results(filename)
    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file, delimiter=";"))
    assert rows[0]["final_score"] == "90.0"

