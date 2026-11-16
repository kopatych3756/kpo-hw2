from pos.domain.models import Student
from pos.infrastructure.json_repositories import JsonStudentRepository


def test_students_saved_to_json(tmp_path):
    filename = tmp_path / "students.json"
    repository = JsonStudentRepository(filename)
    repository.add(Student(1, "Иван Иванов"))
    new_repository = JsonStudentRepository(filename)
    assert new_repository.get(1).name == "Иван Иванов"

def test_students_updated_in_json(tmp_path):
    filename = tmp_path / "students.json"
    repository = JsonStudentRepository(filename)
    repository.add(Student(1, "Иван"))
    repository.update(Student(1, "Пётр"))
    new_repository = JsonStudentRepository(filename)
    assert new_repository.get(1).name == "Пётр"

def test_students_deleted_from_json(tmp_path):
    filename = tmp_path / "students.json"
    repository = JsonStudentRepository(filename)
    repository.add(Student(1, "Иван"))
    repository.delete(1)
    new_repository = JsonStudentRepository(filename)
    assert new_repository.get_all() == []

