from pos.domain.models import Student, Criterion, DomainError


class PosFacade:
    def __init__(self, student_repository, rubric_repository, evaluation_service, exporter=None):
        self.students = student_repository
        self.rubrics = rubric_repository
        self.evaluation_service = evaluation_service
        self.exporter = exporter

    def add_student(self, student_id, name):
        student = Student(student_id, name)
        self.students.add(student)

    def get_student(self, student_id):
        return self.students.get(student_id)

    def get_all_students(self):
        return self.students.get_all()

    def update_student(self, student_id, name):
        self.students.update(Student(student_id, name))

    def delete_student(self, student_id):
        self.students.get(student_id)
        if self.evaluation_service.get_evaluations(student_id):
            raise DomainError("Сначала удалите оценки студента")
        self.students.delete(student_id)

    def add_criterion(self, criterion_id, name, max_score, weight):
        criterion = Criterion(criterion_id, name, max_score, weight)
        rubric = self.rubrics.get()
        rubric.add_criterion(criterion)
        self.rubrics.save(rubric)

    def get_all_criteria(self):
        return self.rubrics.get().get_all_criteria()

    def add_evaluation(self, student_id, criterion_id, score):
        return self.evaluation_service.add_evaluation(student_id, criterion_id, score)

    def update_evaluation(self, student_id, criterion_id, score):
        return self.evaluation_service.update_evaluation(student_id, criterion_id, score)

    def delete_evaluation(self, student_id, criterion_id):
        self.evaluation_service.delete_evaluation(student_id, criterion_id)

    def get_evaluations(self, student_id):
        return self.evaluation_service.get_evaluations(student_id)

    def get_final_score(self, student_id):
        return self.evaluation_service.get_final_score(student_id)

    def export_results(self, filename):
        if self.exporter is None:
            raise DomainError("Экспорт не настроен")
        rows = []
        for student in self.get_all_students():
            final_score = self.get_final_score(student.id)
            rows.append({
                "student_id": student.id,
                "student_name": student.name,
                "final_score": final_score})
        return self.exporter.export(rows, filename)

