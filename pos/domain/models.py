from math import isfinite


class DomainError(ValueError):
    """Ошибка нарушения правила предметной области."""


class Student:
    def __init__(self, student_id: int, name: str):
        if type(student_id) is not int or student_id <= 0:
            raise DomainError("ID студента должен быть больше 0")
        if not isinstance(name, str) or not name.strip():
            raise DomainError("Имя студента не может быть пустым")
        self._id = student_id
        self._name = name.strip()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name


class Criterion:
    def __init__(self, criterion_id: int, name: str, max_score: float, weight: float):
        if type(criterion_id) is not int or criterion_id <= 0:
            raise DomainError("ID критерия должен быть больше 0")
        if not isinstance(name, str) or not name.strip():
            raise DomainError("Название критерия не может быть пустым")
        if not isfinite(max_score) or max_score <= 0:
            raise DomainError("Максимальный балл должен быть больше 0")
        if not isfinite(weight) or weight <= 0:
            raise DomainError("Вес должен быть больше 0")
        self._id = criterion_id
        self._name = name.strip()
        self._max_score = max_score
        self._weight = weight

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def max_score(self):
        return self._max_score

    @property
    def weight(self):
        return self._weight


class Score:
    def __init__(self, value: float):
        if type(value) not in (int, float) or not isfinite(value) or value < 0:
            raise DomainError("Оценка должна быть неотрицательным конечным числом")
        self._value = value

    @property
    def value(self):
        return self._value

    def __eq__(self, other):
        if not isinstance(other, Score):
            return NotImplemented
        return self.value == other.value


class Rubric:
    def __init__(self):
        self._criteria = {}

    def add_criterion(self, criterion: Criterion):
        if criterion.id in self._criteria:
            raise DomainError("Такой критерий уже существует")
        self._criteria[criterion.id] = criterion

    def get_criterion(self, criterion_id: int):
        if criterion_id not in self._criteria:
            raise DomainError("Критерий не найден")
        return self._criteria[criterion_id]

    def get_all_criteria(self):
        return list(self._criteria.values())


class Evaluation:
    def __init__(self, student: Student, criterion_id: int, score: Score, rubric: Rubric):
        criterion = rubric.get_criterion(criterion_id)
        if score.value > criterion.max_score:
            raise DomainError("Оценка превышает максимальный балл критерия")
        self._student_id = student.id
        self._criterion_id = criterion_id
        self._score = score

    @property
    def student_id(self):
        return self._student_id

    @property
    def criterion_id(self):
        return self._criterion_id

    @property
    def score(self):
        return self._score


