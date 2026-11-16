import pytest
from pos.domain.models import Student, Criterion, Rubric, DomainError
from pos.application.evaluation_service import EvaluationService
from pos.infrastructure.memory_repositories import InMemoryStudentRepository, InMemoryRubricRepository, InMemoryEvaluationRepository


def create_service():
    students = InMemoryStudentRepository()
    rubrics = InMemoryRubricRepository()
    evaluations = InMemoryEvaluationRepository()
    students.add(Student(1, "Иван Иванов"))
    rubric = Rubric()
    rubric.add_criterion(Criterion(1, "Домашнее задание", 10, 2))
    rubric.add_criterion(Criterion(2, "Семинары", 5, 1))
    rubrics.save(rubric)
    return EvaluationService(students, rubrics, evaluations)

def test_add_evaluation():
    service = create_service()
    evaluation = service.add_evaluation(1, 1, 8)
    assert evaluation.score.value == 8
    assert len(service.get_evaluations(1)) == 1

def test_update_evaluation():
    service = create_service()
    service.add_evaluation(1, 1, 8)
    service.update_evaluation(1, 1, 9)
    assert service.get_evaluations(1)[0].score.value == 9

def test_delete_evaluation():
    service = create_service()
    service.add_evaluation(1, 1, 8)
    service.delete_evaluation(1, 1)
    assert service.get_evaluations(1) == []

def test_final_score():
    service = create_service()
    service.add_evaluation(1, 1, 8)
    service.add_evaluation(1, 2, 5)
    assert service.get_final_score(1) == 86.67

def test_invalid_score():
    service = create_service()
    with pytest.raises(DomainError):
        service.add_evaluation(1, 1, 15)

def test_unknown_student():
    service = create_service()
    with pytest.raises(DomainError):
        service.add_evaluation(999, 1, 8)

def test_unknown_criterion():
    service = create_service()
    with pytest.raises(DomainError):
        service.add_evaluation(1, 999, 8)

def test_duplicate_evaluation():
    service = create_service()
    service.add_evaluation(1, 1, 8)
    with pytest.raises(DomainError):
        service.add_evaluation(1, 1, 9)

