from pathlib import Path
from pos.domain.models import Rubric
from pos.application.evaluation_service import EvaluationService
from pos.application.facade import PosFacade
from pos.infrastructure.memory_repositories import InMemoryStudentRepository, InMemoryRubricRepository, InMemoryEvaluationRepository
from pos.infrastructure.json_repositories import JsonStudentRepository, JsonRubricRepository, JsonEvaluationRepository
from pos.infrastructure.csv_exporter import CsvExporter


class Container:
    def __init__(self, data_dir=None):
        if data_dir is None:
            self.students = InMemoryStudentRepository()
            self.rubrics = InMemoryRubricRepository()
            self.evaluations = InMemoryEvaluationRepository()
            self.rubrics.save(Rubric())
        else:
            data_dir = Path(data_dir)
            self.students = JsonStudentRepository(data_dir / "students.json")
            self.rubrics = JsonRubricRepository(data_dir / "rubric.json")
            self.evaluations = JsonEvaluationRepository(self.students, self.rubrics, data_dir / "evaluations.json")
        self.evaluation_service = EvaluationService(self.students, self.rubrics, self.evaluations)
        self.exporter = CsvExporter()
        self.app = PosFacade(self.students, self.rubrics, self.evaluation_service, self.exporter)

    def create_app(self):
        return self.app
