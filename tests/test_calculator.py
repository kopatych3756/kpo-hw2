import pytest
from pos.domain.models import Student, Criterion, Rubric, DomainError
from pos.domain.factories import EvaluationFactory
from pos.domain.services import FinalScoreCalculator, MissingAsZeroStrategy, GradedOnlyStrategy


def create_test_data():
    student = Student(1, "Иван Иванов")
    rubric = Rubric()
    rubric.add_criterion(Criterion(1, "Домашнее задание", 10, 2))
    rubric.add_criterion(Criterion(2, "Семинары", 5, 1))
    rubric.add_criterion(Criterion(3, "Контрольная", 10, 3))
    factory = EvaluationFactory(rubric)
    return student, rubric, factory

def test_final_score():
    student, rubric, factory = create_test_data()
    evaluations = [factory.create(student, 1, 8), factory.create(student, 2, 5), factory.create(student, 3, 7)]
    calculator = FinalScoreCalculator(MissingAsZeroStrategy())
    result = calculator.calculate(student.id, rubric, evaluations)
    assert result == 78.33

def test_missing_grades_as_zero():
    student, rubric, factory = create_test_data()
    evaluations = [factory.create(student, 1, 8)]
    calculator = FinalScoreCalculator(MissingAsZeroStrategy())
    result = calculator.calculate(student.id, rubric, evaluations)
    assert result == 26.67

def test_only_graded_criteria():
    student, rubric, factory = create_test_data()
    evaluations = [factory.create(student, 1, 8)]
    calculator = FinalScoreCalculator(GradedOnlyStrategy())
    result = calculator.calculate(student.id, rubric, evaluations)
    assert result == 80.0

def test_no_evaluations():
    student, rubric, _ = create_test_data()
    calculator = FinalScoreCalculator(GradedOnlyStrategy())
    assert calculator.calculate(student.id, rubric, []) == 0.0

def test_duplicate_evaluations():
    student, rubric, factory = create_test_data()
    evaluation = factory.create(student, 1, 8)
    calculator = FinalScoreCalculator(MissingAsZeroStrategy())
    with pytest.raises(DomainError):
        calculator.calculate(student.id, rubric, [evaluation, evaluation])

def test_other_student_evaluation():
    student, rubric, factory = create_test_data()
    other_student = Student(2, "Мария Петрова")
    evaluation = factory.create(other_student, 1, 8)
    calculator = FinalScoreCalculator(MissingAsZeroStrategy())
    with pytest.raises(DomainError):
        calculator.calculate(student.id, rubric, [evaluation])



