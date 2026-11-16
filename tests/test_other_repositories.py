import pytest
from pos.domain.models import Student, Criterion, Rubric, DomainError
from pos.domain.factories import EvaluationFactory
from pos.infrastructure.memory_repositories import InMemoryRubricRepository, InMemoryEvaluationRepository


def create_evaluation(score):
    student = Student(1, "Иван Иванов")
    rubric = Rubric()
    rubric.add_criterion(Criterion(1, "Домашка", 10, 2))
    factory = EvaluationFactory(rubric)
    return factory.create(student, 1, score)

def test_save_rubric():
    repository = InMemoryRubricRepository()
    rubric = Rubric()
    rubric.add_criterion(Criterion(1, "Домашка", 10, 2))
    repository.save(rubric)
    assert repository.get().get_criterion(1).name == "Домашка"

def test_get_missing_rubric():
    repository = InMemoryRubricRepository()
    with pytest.raises(DomainError):
        repository.get()

def test_add_evaluation():
    repository = InMemoryEvaluationRepository()
    evaluation = create_evaluation(8)
    repository.add(evaluation)
    assert repository.get(1, 1).score.value == 8
    assert len(repository.get_for_student(1)) == 1

def test_duplicate_evaluation():
    repository = InMemoryEvaluationRepository()
    repository.add(create_evaluation(8))
    with pytest.raises(DomainError):
        repository.add(create_evaluation(9))

def test_update_evaluation():
    repository = InMemoryEvaluationRepository()
    repository.add(create_evaluation(8))
    repository.update(create_evaluation(9))
    assert repository.get(1, 1).score.value == 9

def test_delete_evaluation():
    repository = InMemoryEvaluationRepository()
    repository.add(create_evaluation(8))
    repository.delete(1, 1)
    assert repository.get_for_student(1) == []

