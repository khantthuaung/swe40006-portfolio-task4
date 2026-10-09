"""Read student marks from CSV and save a text report. No web server is used."""
import argparse
import csv
import math
from pathlib import Path
import sys


def grade_for(mark):
    # Demonstration boundaries; change these if your unit uses another scheme.
    if mark >= 80:
        return "HD"
    if mark >= 70:
        return "D"
    if mark >= 60:
        return "C"
    if mark >= 50:
        return "P"
    return "F"


def read_students(filename):
    students = []
    errors = []
    seen_ids = set()
    with open(filename, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required = {"student_id", "name", "mark"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV must contain student_id,name,mark headers.")
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("CSV headers must not be duplicated.")
        for row in reader:
            # Reject invalid records but still analyse the valid records.
            student_id = (row.get("student_id") or "").strip()
            name = (row.get("name") or "").strip()
            reason = ""
            if None in row:
                reason = "Too many columns."
            elif not student_id or not name:
                reason = "Student ID and name are required."
            elif student_id in seen_ids:
                reason = "Duplicate student ID."
            else:
                try:
                    mark = float((row.get("mark") or "").strip())
                    if not math.isfinite(mark) or not 0 <= mark <= 100:
                        reason = "Mark must be between 0 and 100."
                except ValueError:
                    reason = "Mark must be a number."
            if reason:
                errors.append(f"Line {reader.line_num}: {reason}")
                continue
            seen_ids.add(student_id)
            students.append({"id": student_id, "name": name,
                             "mark": mark, "grade": grade_for(mark)})
    return students, errors


def make_report(students, errors):
    marks = [student["mark"] for student in students]
    lines = ["STUDENT MARKS ANALYSIS", "=" * 36,
             f"Valid students: {len(students)}", f"Rejected records: {len(errors)}"]
    if marks:
        passed = sum(mark >= 50 for mark in marks)
        lines.extend([f"Average mark: {sum(marks) / len(marks):.2f}",
                      f"Highest mark: {max(marks):.2f}",
                      f"Lowest mark: {min(marks):.2f}",
                      f"Pass rate: {passed / len(marks) * 100:.2f}%"])
    else:
        lines.append("No valid marks to analyse.")
    lines.extend(["", "GRADE DISTRIBUTION (demonstration boundaries)",
                  "HD: 80–100 | D: 70–<80 | C: 60–<70 | P: 50–<60 | F: <50"])
    for grade in ["HD", "D", "C", "P", "F"]:
        count = sum(student["grade"] == grade for student in students)
        lines.append(f"{grade}: {count}")
    lines.extend(["", "VALID STUDENT RESULTS"])
    for student in students:
        lines.append(f"{student['id']} | {student['name']} | "
                     f"{student['mark']:.2f} | {student['grade']}")
    lines.extend(["", "VALIDATION ERRORS"])
    lines.extend(errors or ["None"])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="/data/students.csv")
    parser.add_argument("--output", default="/output/report.txt")
    args = parser.parse_args()
    try:
        output = Path(args.output)
        # Protect the source CSV from accidental replacement by the report.
        if Path(args.input).resolve() == output.resolve():
            raise ValueError("Input and output paths must be different.")
        students, errors = read_students(args.input)
        report = make_report(students, errors)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
        print(report)
        print(f"Report saved to: {output}")
        if not students:
            return 1
        if errors:
            print("Completed with rejected records; see validation errors above.")
            return 2
        return 0
    except (OSError, ValueError, UnicodeError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
