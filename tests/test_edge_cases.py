import csv
import pytest
from pos.domain.models import DomainError
from pos.infrastructure.container import Container


def create_app():
    app = Container().create_app()
    app.add_student(1, "Иван")
    app.add_criterion(1, "Домашка", 10, 2)
    return app

@pytest.mark.parametrize("score", [-1, 11, float("nan"), float("inf")])
def test_invalid_scores(score):
    app = create_app()
    with pytest.raises(DomainError):
        app.add_evaluation(1, 1, score)

def test_invalid_update_keeps_old_score():
    app = create_app()
    app.add_evaluation(1, 1, 8)
    with pytest.raises(DomainError):
        app.update_evaluation(1, 1, 100)
    assert app.get_final_score(1) == 80.0

def test_cannot_delete_student_with_evaluation():
    app = create_app()
    app.add_evaluation(1, 1, 8)
    with pytest.raises(DomainError):
        app.delete_student(1)
    assert app.get_student(1).name == "Иван"

def test_json_and_csv_together(tmp_path):
    data_dir = tmp_path / "data"
    app = Container(data_dir=data_dir).create_app()
    app.add_student(1, "Иван")
    app.add_criterion(1, "Домашка", 10, 2)
    app.add_evaluation(1, 1, 8)
    app2 = Container(data_dir=data_dir).create_app()
    assert app2.get_final_score(1) == 80.0
    
    filename = tmp_path / "results.csv"
    app2.export_results(filename)
    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file, delimiter=";"))
    assert len(rows) == 1
    assert rows[0]["student_name"] == "Иван"
    assert rows[0]["final_score"] == "80.0"


