import pytest
from pos.domain.models import Student, Criterion, Rubric, DomainError
from pos.domain.factories import EvaluationFactory


def create_test_data():
    student = Student(1, "Иван Иванов")
    rubric = Rubric()
    rubric.add_criterion(Criterion(1, "Домашнее задание", 10, 2))
    factory = EvaluationFactory(rubric)
    return student, factory

def test_valid_evaluation():
    student, factory = create_test_data()
    evaluation = factory.create(student, 1, 8)
    assert evaluation.student_id == 1
    assert evaluation.criterion_id == 1
    assert evaluation.score.value == 8

def test_max_score():
    student, factory = create_test_data()
    evaluation = factory.create(student, 1, 10)
    assert evaluation.score.value == 10

def test_zero_score():
    student, factory = create_test_data()
    evaluation = factory.create(student, 1, 0)
    assert evaluation.score.value == 0

def test_score_above_maximum():
    student, factory = create_test_data()
    with pytest.raises(DomainError):
        factory.create(student, 1, 15)

def test_negative_score():
    student, factory = create_test_data()
    with pytest.raises(DomainError):
        factory.create(student, 1, -5)

def test_unknown_criterion():
    student, factory = create_test_data()
    with pytest.raises(DomainError):
        factory.create(student, 999, 8)


