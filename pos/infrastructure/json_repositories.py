import json
from pathlib import Path
from pos.domain.models import Student, Criterion, Rubric, DomainError
from pos.domain.factories import EvaluationFactory
from pos.domain.repositories import StudentRepository, RubricRepository, EvaluationRepository


class JsonStudentRepository(StudentRepository):
    def __init__(self, filename="data/students.json"):
        self.filename = Path(filename)
        self._students = {}
        if self.filename.exists():
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            for item in data:
                student = Student(item["id"], item["name"])
                if student.id in self._students:
                    raise DomainError("В JSON обнаружен повторяющийся ID студента")
                self._students[student.id] = student

    def _save(self):
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        data = []
        for student in self._students.values():
            data.append({"id": student.id, "name": student.name})
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add(self, student):
        if student.id in self._students:
            raise DomainError("Студент с таким ID уже существует")
        self._students[student.id] = student
        self._save()

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
        self._save()

    def delete(self, student_id):
        if student_id not in self._students:
            raise DomainError("Студент не найден")
        del self._students[student_id]
        self._save()


class JsonRubricRepository(RubricRepository):
    def __init__(self, filename="data/rubric.json"):
        self.filename = Path(filename)
        self._rubric = Rubric()
        if self.filename.exists():
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            for item in data:
                criterion = Criterion(
                    item["id"],
                    item["name"],
                    item["max_score"],
                    item["weight"])
                self._rubric.add_criterion(criterion)

    def get(self):
        return self._rubric

    def save(self, rubric):
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        data = []
        for criterion in rubric.get_all_criteria():
            data.append({
                "id": criterion.id,
                "name": criterion.name,
                "max_score": criterion.max_score,
                "weight": criterion.weight})
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        self._rubric = rubric


class JsonEvaluationRepository(EvaluationRepository):
    def __init__(self, student_repository, rubric_repository, filename="data/evaluations.json"):
        self.filename = Path(filename)
        self.students = student_repository
        self.rubrics = rubric_repository
        self._evaluations = {}
        if self.filename.exists():
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            factory = EvaluationFactory(self.rubrics.get())
            for item in data:
                student = self.students.get(item["student_id"])
                evaluation = factory.create(student, item["criterion_id"], item["score"])
                key = (evaluation.student_id, evaluation.criterion_id)
                if key in self._evaluations:
                    raise DomainError("В файле найдены повторяющиеся оценки")
                self._evaluations[key] = evaluation

    def _save(self):
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        data = []
        for evaluation in self._evaluations.values():
            data.append({
                "student_id": evaluation.student_id,
                "criterion_id": evaluation.criterion_id,
                "score": evaluation.score.value})
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add(self, evaluation):
        key = (evaluation.student_id, evaluation.criterion_id)
        if key in self._evaluations:
            raise DomainError("Оценка уже выставлена")
        self._evaluations[key] = evaluation
        self._save()

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
        self._save()

    def delete(self, student_id, criterion_id):
        key = (student_id, criterion_id)
        if key not in self._evaluations:
            raise DomainError("Оценка не найдена")
        del self._evaluations[key]
        self._save()

