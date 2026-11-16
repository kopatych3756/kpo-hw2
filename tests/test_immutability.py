import pytest
from pos.domain.models import Student, Criterion, Score, Rubric
from pos.domain.factories import EvaluationFactory


def test_student_name_cannot_be_changed():
    student = Student(1, "Иван")
    with pytest.raises(AttributeError):
        student.name = ""

def test_criterion_max_score_cannot_be_changed():
    criterion = Criterion(1, "Домашка", 10, 2)
    with pytest.raises(AttributeError):
        criterion.max_score = -100

def test_score_cannot_be_changed():
    score = Score(8)
    with pytest.raises(AttributeError):
        score.value = -5

def test_score_equality():
    score1 = Score(8)
    score2 = Score(8)
    assert score1 == score2

def test_evaluation_cannot_be_changed():
    student = Student(1, "Иван")
    rubric = Rubric()
    rubric.add_criterion(Criterion(1, "Домашка", 10, 2))
    factory = EvaluationFactory(rubric)
    evaluation = factory.create(student, 1, 8)
    with pytest.raises(AttributeError):
        evaluation.score = Score(15)

