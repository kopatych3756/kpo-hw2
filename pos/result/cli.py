from pos.domain.models import DomainError


class ConsoleUI:
    def __init__(self, app):
        self.app = app

    def run(self):
        actions = {
            "1": self.add_student,
            "2": self.show_students,
            "3": self.update_student,
            "4": self.delete_student,
            "5": self.add_criterion,
            "6": self.show_criteria,
            "7": self.add_evaluation,
            "8": self.show_evaluations,
            "9": self.update_evaluation,
            "10": self.delete_evaluation,
            "11": self.show_final_score,
            "12": self.export_results,
        }
        while True:
            print("\nПОС")
            print("1. Добавить студента")
            print("2. Показать студентов")
            print("3. Изменить имя студента")
            print("4. Удалить студента")
            print("5. Добавить критерий")
            print("6. Показать критерии")
            print("7. Выставить оценку")
            print("8. Показать оценки студента")
            print("9. Исправить оценку")
            print("10. Отменить оценку")
            print("11. Рассчитать итог")
            print("12. Экспортировать итоги в CSV")
            print("0. Выход")
            try:
                command = input("Выберите действие: ").strip()
                if command == "0":
                    print("Чао какао!")
                    break
                action = actions.get(command)
                if action is None:
                    print("Неизвестная команда")
                    continue
                action()
            except DomainError as error:
                print(f"Ошибка: {error}")
            except ValueError:
                print("Ошибка: введите корректное число")
            except (EOFError, KeyboardInterrupt):
                print("Выход из программы")
                break
            except OSError as error:
                print(f"Ошибка при работе с файлом: {error}")
                break

    def add_student(self):
        student_id = int(input("ID студента: "))
        name = input("Имя студента: ")
        self.app.add_student(student_id, name)
        print("Студент добавлен")

    def show_students(self):
        students = self.app.get_all_students()
        if not students:
            print("Студентов пока нет")
            return
        for student in students:
            print(f"{student.id}: {student.name}")

    def update_student(self):
        student_id = int(input("ID студента: "))
        name = input("Новое имя: ")
        self.app.update_student(student_id, name)
        print("Имя студента изменено")

    def delete_student(self):
        student_id = int(input("ID студента: "))
        self.app.delete_student(student_id)
        print("Студент удалён")

    def add_criterion(self):
        criterion_id = int(input("ID критерия: "))
        name = input("Название критерия: ")
        max_score = float(input("Максимальный балл: "))
        weight = float(input("Вес: "))
        self.app.add_criterion(criterion_id, name, max_score, weight)
        print("Критерий добавлен")

    def show_criteria(self):
        criteria = self.app.get_all_criteria()
        if not criteria:
            print("Критериев пока нет")
            return
        for criterion in criteria:
            print(f"{criterion.id}: {criterion.name}, максимум {criterion.max_score}, вес {criterion.weight}")

    def add_evaluation(self):
        student_id = int(input("ID студента: "))
        criterion_id = int(input("ID критерия: "))
        score = float(input("Балл: "))
        self.app.add_evaluation(student_id, criterion_id, score)
        print("Оценка выставлена")

    def show_evaluations(self):
        student_id = int(input("ID студента: "))
        evaluations = self.app.get_evaluations(student_id)
        if not evaluations:
            print("Оценок пока нет")
            return
        criteria = {criterion.id: criterion for criterion in self.app.get_all_criteria()}
        for evaluation in evaluations:
            criterion = criteria[evaluation.criterion_id]
            print(f"{criterion.name}: {evaluation.score.value} из {criterion.max_score}")

    def update_evaluation(self):
        student_id = int(input("ID студента: "))
        criterion_id = int(input("ID критерия: "))
        score = float(input("Новый балл: "))
        self.app.update_evaluation(student_id, criterion_id, score)
        print("Оценка исправлена")

    def delete_evaluation(self):
        student_id = int(input("ID студента: "))
        criterion_id = int(input("ID критерия: "))
        self.app.delete_evaluation(student_id, criterion_id)
        print("Оценка отменена")

    def show_final_score(self):
        student_id = int(input("ID студента: "))
        student = self.app.get_student(student_id)
        score = self.app.get_final_score(student_id)
        print(f"Итог для {student.name}: {score}%")

    def export_results(self):
        filename = "data/results.csv"
        path = self.app.export_results(filename)
        print(f"Итоги экспортированы в файл: {path}")

