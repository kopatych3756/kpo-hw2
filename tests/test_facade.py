import pytest
from pos.domain.models import DomainError
from pos.infrastructure.container import Container


def test_facade_add_student():
    app = Container().create_app()
    app.add_student(1, "Иван")
    assert app.get_student(1).name == "Иван"

def test_facade_add_criterion_and_evaluation():
    app = Container().create_app()
    app.add_student(1, "Иван")
    app.add_criterion(1, "Домашка", 10, 2)
    app.add_evaluation(1, 1, 8)
    assert app.get_final_score(1) == 80.0

def test_facade_rejects_delete_student_with_grades():
    app = Container().create_app()
    app.add_student(1, "Иван")
    app.add_criterion(1, "Домашка", 10, 2)
    app.add_evaluation(1, 1, 8)
    with pytest.raises(DomainError):
        app.delete_student(1)

def test_facade_change_grade():
    app = Container().create_app()
    app.add_student(1, "Иван")
    app.add_criterion(1, "Домашка", 10, 2)
    app.add_evaluation(1, 1, 8)
    app.update_evaluation(1, 1, 9)
    assert app.get_final_score(1) == 90.0

