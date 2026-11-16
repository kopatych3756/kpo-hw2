from pos.domain.models import Evaluation, Score, Rubric, Student


class EvaluationFactory:
    def __init__(self, rubric: Rubric):
        self.rubric = rubric

    def create(self, student: Student, criterion_id: int, score_value: float):
        score = Score(score_value)
        return Evaluation(student, criterion_id, score, self.rubric)
