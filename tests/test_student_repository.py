import pytest
from pos.domain.models import Student, DomainError
from pos.infrastructure.memory_repositories import InMemoryStudentRepository


def test_add_student():
    repository = InMemoryStudentRepository()
    repository.add(Student(1, "Иван"))
    assert repository.get(1).name == "Иван"

def test_duplicate_student():
    repository = InMemoryStudentRepository()
    repository.add(Student(1, "Иван"))
    with pytest.raises(DomainError):
        repository.add(Student(1, "Мария"))

def test_get_unknown_student():
    repository = InMemoryStudentRepository()
    with pytest.raises(DomainError):
        repository.get(999)

def test_update_student():
    repository = InMemoryStudentRepository()
    repository.add(Student(1, "Иван"))
    repository.update(Student(1, "Пётр"))
    assert repository.get(1).name == "Пётр"

def test_delete_student():
    repository = InMemoryStudentRepository()
    repository.add(Student(1, "Иван"))
    repository.delete(1)
    assert repository.get_all() == []
