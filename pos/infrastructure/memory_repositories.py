from pos.domain.models import DomainError
from pos.domain.repositories import StudentRepository, RubricRepository, EvaluationRepository


class InMemoryStudentRepository(StudentRepository):
    def __init__(self):
        self._students = {}

    def add(self, student):
        if student.id in self._students:
            raise DomainError("Студент с таким ID уже существует")
        self._students[student.id] = student

    def get(self, student_id):
        if student_id not in self._students:
            raise DomainError("Студент не найден")
        return self._students[student_id]

    def get_all(self):
        return list(self._students.values())

    def update(self, student):
        if student.id not in self._students:
            raise DomainError("Студент не найден")
        self._students[student.id] = student

    def delete(self, student_id):
        if student_id not in self._students:
            raise DomainError("Студент не найден")
        del self._students[student_id]


class InMemoryRubricRepository(RubricRepository):
    def __init__(self):
        self._rubric = None

    def save(self, rubric):
        self._rubric = rubric

    def get(self):
        if self._rubric is None:
            raise DomainError("Рубрикатор ещё не создан")
        return self._rubric


class InMemoryEvaluationRepository(EvaluationRepository):
    def __init__(self):
        self._evaluations = {}

    def add(self, evaluation):
        key = (evaluation.student_id, evaluation.criterion_id)
        if key in self._evaluations:
            raise DomainError("Оценка уже выставлена")
        self._evaluations[key] = evaluation

    def get(self, student_id, criterion_id):
        key = (student_id, criterion_id)
        if key not in self._evaluations:
            raise DomainError("Оценка не найдена")
        return self._evaluations[key]

    def get_for_student(self, student_id):
        return [evaluation for evaluation in self._evaluations.values() if evaluation.student_id == student_id]

    def update(self, evaluation):
        key = (evaluation.student_id, evaluation.criterion_id)
        if key not in self._evaluations:
            raise DomainError("Оценка не найдена")
        self._evaluations[key] = evaluation

    def delete(self, student_id, criterion_id):
        key = (student_id, criterion_id)
        if key not in self._evaluations:
            raise DomainError("Оценка не найдена")
        del self._evaluations[key]

