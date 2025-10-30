import csv
import os
from typing import Dict, List, Optional, Iterable, Tuple

from .models import Student, Course, Professor, Grade, LoginUser

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class CsvPaths:
	students = os.path.join(_DATA_DIR, "students.csv")
	courses = os.path.join(_DATA_DIR, "courses.csv")
	professors = os.path.join(_DATA_DIR, "professors.csv")
	grades = os.path.join(_DATA_DIR, "grades.csv")
	logins = os.path.join(_DATA_DIR, "logins.csv")


def ensure_data_dir() -> None:
	os.makedirs(_DATA_DIR, exist_ok=True)


class StudentRepo:
	FIELDS = ["email_address", "first_name", "last_name", "course_id", "grade", "marks"]

	def __init__(self, path: Optional[str] = None):
		self.path = path or CsvPaths.students
		ensure_data_dir()

	def load_all(self) -> List[Student]:
		if not os.path.exists(self.path):
			return []
		rows: List[Student] = []
		with open(self.path, newline="", encoding="utf-8") as f:
			for r in csv.DictReader(f):
				rows.append(
					Student(
						email_address=r["email_address"],
						first_name=r["first_name"],
						last_name=r["last_name"],
						course_id=r["course_id"],
						grade=r["grade"],
						marks=float(r["marks"]),
					)
				)
		return rows

	def save_all(self, students: Iterable[Student]) -> None:
		ensure_data_dir()
		with open(self.path, "w", newline="", encoding="utf-8") as f:
			w = csv.DictWriter(f, fieldnames=self.FIELDS)
			w.writeheader()
			for s in students:
				w.writerow(
					{
						"email_address": s.email_address,
						"first_name": s.first_name,
						"last_name": s.last_name,
						"course_id": s.course_id,
						"grade": s.grade,
						"marks": f"{s.marks}",
					}
				)


class CourseRepo:
	FIELDS = ["course_id", "course_name", "description", "credits"]

	def __init__(self, path: Optional[str] = None):
		self.path = path or CsvPaths.courses
		ensure_data_dir()

	def load_all(self) -> List[Course]:
		if not os.path.exists(self.path):
			return []
		rows: List[Course] = []
		with open(self.path, newline="", encoding="utf-8") as f:
			for r in csv.DictReader(f):
				credits = int(r["credits"]) if r.get("credits") else None
				rows.append(
					Course(
						course_id=r["course_id"],
						course_name=r["course_name"],
						description=r.get("description", ""),
						credits=credits,
					)
				)
		return rows

	def save_all(self, courses: Iterable[Course]) -> None:
		ensure_data_dir()
		with open(self.path, "w", newline="", encoding="utf-8") as f:
			w = csv.DictWriter(f, fieldnames=self.FIELDS)
			w.writeheader()
			for c in courses:
				w.writerow(
					{
						"course_id": c.course_id,
						"course_name": c.course_name,
						"description": c.description,
						"credits": c.credits if c.credits is not None else "",
					}
				)


class ProfessorRepo:
	FIELDS = ["professor_id", "name", "rank", "course_id", "email_address"]

	def __init__(self, path: Optional[str] = None):
		self.path = path or CsvPaths.professors
		ensure_data_dir()

	def load_all(self) -> List[Professor]:
		if not os.path.exists(self.path):
			return []
		rows: List[Professor] = []
		with open(self.path, newline="", encoding="utf-8") as f:
			for r in csv.DictReader(f):
				rows.append(
					Professor(
						professor_id=r["professor_id"],
						name=r["name"],
						rank=r["rank"],
						course_id=r["course_id"],
						email_address=r.get("email_address") or None,
					)
				)
		return rows

	def save_all(self, professors: Iterable[Professor]) -> None:
		ensure_data_dir()
		with open(self.path, "w", newline="", encoding="utf-8") as f:
			w = csv.DictWriter(f, fieldnames=self.FIELDS)
			w.writeheader()
			for p in professors:
				w.writerow(
					{
						"professor_id": p.professor_id,
						"name": p.name,
						"rank": p.rank,
						"course_id": p.course_id,
						"email_address": p.email_address or "",
					}
				)


class GradeRepo:
	FIELDS = ["grade_id", "grade", "marks_range"]

	def __init__(self, path: Optional[str] = None):
		self.path = path or CsvPaths.grades
		ensure_data_dir()

	def load_all(self) -> List[Grade]:
		if not os.path.exists(self.path):
			return []
		rows: List[Grade] = []
		with open(self.path, newline="", encoding="utf-8") as f:
			for r in csv.DictReader(f):
				rows.append(Grade(grade_id=r["grade_id"], grade=r["grade"], marks_range=r["marks_range"]))
		return rows

	def save_all(self, grades: Iterable[Grade]) -> None:
		ensure_data_dir()
		with open(self.path, "w", newline="", encoding="utf-8") as f:
			w = csv.DictWriter(f, fieldnames=self.FIELDS)
			w.writeheader()
			for g in grades:
				w.writerow({"grade_id": g.grade_id, "grade": g.grade, "marks_range": g.marks_range})


class LoginRepo:
	FIELDS = ["user_id", "password_encrypted", "role"]

	def __init__(self, path: Optional[str] = None):
		self.path = path or CsvPaths.logins
		ensure_data_dir()

	def load_all(self) -> List[LoginUser]:
		if not os.path.exists(self.path):
			return []
		rows: List[LoginUser] = []
		with open(self.path, newline="", encoding="utf-8") as f:
			for r in csv.DictReader(f):
				rows.append(LoginUser(user_id=r["user_id"], password_encrypted=r["password_encrypted"], role=r["role"]))
		return rows

	def save_all(self, users: Iterable[LoginUser]) -> None:
		ensure_data_dir()
		with open(self.path, "w", newline="", encoding="utf-8") as f:
			w = csv.DictWriter(f, fieldnames=self.FIELDS)
			w.writeheader()
			for u in users:
				w.writerow({"user_id": u.user_id, "password_encrypted": u.password_encrypted, "role": u.role})
