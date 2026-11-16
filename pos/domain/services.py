from math import isfinite
from pos.domain.models import DomainError, Rubric


class MissingAsZeroStrategy:
    def get_criteria(self, criteria, scores):
        return criteria


class GradedOnlyStrategy:
    def get_criteria(self, criteria, scores):
        return [criterion for criterion in criteria if criterion.id in scores]


class FinalScoreCalculator:
    def __init__(self, strategy):
        self.strategy = strategy

    def calculate(self, student_id: int, rubric: Rubric, evaluations: list):
        scores = {}
        for evaluation in evaluations:
            if evaluation.student_id != student_id:
                raise DomainError("Оценка принадлежит другому студенту")
            criterion = rubric.get_criterion(evaluation.criterion_id)
            if evaluation.criterion_id in scores:
                raise DomainError("Для критерия найдено несколько оценок")
            value = evaluation.score.value
            if (not isfinite(value) or value < 0 or value > criterion.max_score):
                raise DomainError("Некорректный балл по критерию")
            scores[evaluation.criterion_id] = value
        criteria = self.strategy.get_criteria(rubric.get_all_criteria(), scores)
        total_weight = 0
        weighted_sum = 0
        for criterion in criteria:
            score = scores.get(criterion.id, 0)
            weighted_sum += (score / criterion.max_score) * criterion.weight
            total_weight += criterion.weight
        if total_weight == 0:
            return 0.0
        result = weighted_sum / total_weight * 100
        return round(result, 2)


