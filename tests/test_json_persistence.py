from pos.infrastructure.container import Container


def test_data_survives_restart(tmp_path):
    app1 = Container(data_dir=tmp_path).create_app()
    app1.add_student(1, "Иван")
    app1.add_criterion(1, "Домашка", 10, 2)
    app1.add_evaluation(1, 1, 8)
    app2 = Container(data_dir=tmp_path).create_app()
    assert app2.get_student(1).name == "Иван"
    assert len(app2.get_all_criteria()) == 1
    assert app2.get_evaluations(1)[0].score.value == 8
    assert app2.get_final_score(1) == 80.0

def test_updated_grade_survives_restart(tmp_path):
    app1 = Container(data_dir=tmp_path).create_app()
    app1.add_student(1, "Иван")
    app1.add_criterion(1, "Домашка", 10, 2)
    app1.add_evaluation(1, 1, 8)
    app1.update_evaluation(1, 1, 9)
    app2 = Container(data_dir=tmp_path).create_app()
    assert app2.get_final_score(1) == 90.0

def test_deleted_grade_survives_restart(tmp_path):
    app1 = Container(data_dir=tmp_path).create_app()
    app1.add_student(1, "Иван")
    app1.add_criterion(1, "Домашка", 10, 2)
    app1.add_evaluation(1, 1, 8)
    app1.delete_evaluation(1, 1)
    app2 = Container(data_dir=tmp_path).create_app()
    assert app2.get_evaluations(1) == []
    assert app2.get_final_score(1) == 0.0

