from pos.domain.factories import EvaluationFactory
from pos.domain.services import FinalScoreCalculator, MissingAsZeroStrategy


class EvaluationService:
    def __init__(self, student_repository, rubric_repository, evaluation_repository):
        self.students = student_repository
        self.rubrics = rubric_repository
        self.evaluations = evaluation_repository

    def add_evaluation(self, student_id, criterion_id, score_value):
        student = self.students.get(student_id)
        rubric = self.rubrics.get()
        factory = EvaluationFactory(rubric)
        evaluation = factory.create(student, criterion_id, score_value)
        self.evaluations.add(evaluation)
        return evaluation

    def update_evaluation(self, student_id, criterion_id, score_value):
        student = self.students.get(student_id)
        rubric = self.rubrics.get()
        factory = EvaluationFactory(rubric)
        evaluation = factory.create(student, criterion_id, score_value)
        self.evaluations.update(evaluation)
        return evaluation

    def delete_evaluation(self, student_id, criterion_id):
        self.students.get(student_id)
        self.evaluations.delete(student_id, criterion_id)

    def get_evaluations(self, student_id):
        self.students.get(student_id)
        return self.evaluations.get_for_student(student_id)

    def get_final_score(self, student_id):
        self.students.get(student_id)
        rubric = self.rubrics.get()
        evaluations = self.evaluations.get_for_student(student_id)
        calculator = FinalScoreCalculator(MissingAsZeroStrategy())
        return calculator.calculate(student_id, rubric, evaluations)

