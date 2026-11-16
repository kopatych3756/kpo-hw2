import csv
from pathlib import Path
from pos.application.ports import ExportPort


class CsvExporter(ExportPort):
    def export(self, rows, filename):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["student_id", "student_name", "final_score"])
            for row in rows:
                writer.writerow([row["student_id"], row["student_name"], row["final_score"]])
        return path
