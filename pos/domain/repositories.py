from abc import ABC, abstractmethod


class StudentRepository(ABC):

    @abstractmethod
    def add(self, student):
        pass
    
    @abstractmethod
    def get(self, student_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, student):
        pass

    @abstractmethod
    def delete(self, student_id):
        pass


class RubricRepository(ABC):

    @abstractmethod
    def save(self, rubric):
        pass

    @abstractmethod
    def get(self):
        pass


class EvaluationRepository(ABC):

    @abstractmethod
    def add(self, evaluation):
        pass

    @abstractmethod
    def get(self, student_id, criterion_id):
        pass

    @abstractmethod
    def get_for_student(self, student_id):
        pass

    @abstractmethod
    def update(self, evaluation):
        pass

    @abstractmethod
    def delete(self, student_id, criterion_id):
        pass

