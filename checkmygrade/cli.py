from __future__ import annotations

import sys
from typing import Optional

from .models import Student, Course
from .services import StudentService, CourseService, ProfessorService, GradeService, AuthService


class CLI:
	def __init__(self) -> None:
		self.students = StudentService()
		self.courses = CourseService()
		self.professors = ProfessorService()
		self.grades = GradeService()
		self.auth = AuthService()

	def run(self) -> None:
		while True:
			print("\nCheckMyGrade - Main Menu")
			print("1. Add Student")
			print("2. Delete Student")
			print("3. Update Student Marks")
			print("4. Sort Students by Marks (desc)")
			print("5. Search Student by Email (timed)")
			print("6. Course Stats (avg/median)")
			print("7. Register/Login User")
			print("0. Exit")
			choice = input("Select: ").strip()
			if choice == "1":
				self._add_student()
			elif choice == "2":
				self._delete_student()
			elif choice == "3":
				self._update_student_marks()
			elif choice == "4":
				self._sort_students()
			elif choice == "5":
				self._search_student_timed()
			elif choice == "6":
				self._course_stats()
			elif choice == "7":
				self._auth_flow()
			elif choice == "0":
				print("Bye.")
				return
			else:
				print("Invalid selection.")

	def _add_student(self) -> None:
		email = input("Email: ").strip()
		first = input("First name: ").strip()
		last = input("Last name: ").strip()
		course = input("Course ID: ").strip()
		grade = input("Grade (e.g., A): ").strip()
		marks = float(input("Marks (0-100): ").strip())
		try:
			self.students.add(Student(email, first, last, course, grade, marks))
			print("Added.")
		except Exception as e:
			print(f"Error: {e}")

	def _delete_student(self) -> None:
		email = input("Email to delete: ").strip()
		ok = self.students.delete(email)
		print("Deleted." if ok else "Not found.")

	def _update_student_marks(self) -> None:
		email = input("Email: ").strip()
		marks = float(input("New marks: ").strip())
		ok = self.students.update(email, marks=marks)
		print("Updated." if ok else "Not found.")

	def _sort_students(self) -> None:
		rows, elapsed = self.students.sort(lambda s: s.marks, reverse=True)
		print(f"Sorted {len(rows)} students by marks desc in {elapsed:.6f}s")
		for s in rows[:10]:
			print(f"{s.email_address}\t{s.marks}")

	def _search_student_timed(self) -> None:
		email = input("Email to search: ").strip().lower()
		import time
		start = time.perf_counter()
		res = self.students.find(lambda s: s.key_email() == email)
		elapsed = time.perf_counter() - start
		print(f"Search took {elapsed:.6f}s; found {len(res)} record(s)")
		for s in res:
			print(f"{s.email_address} -> {s.first_name} {s.last_name}, {s.course_id}, {s.marks}")

	def _course_stats(self) -> None:
		cid = input("Course ID: ").strip()
		avg, med = self.students.stats_for_course(cid)
		print(f"avg={avg} median={med}")

	def _auth_flow(self) -> None:
		print("1) Register 2) Login 3) Change Password")
		c = input(": ").strip()
		if c == "1":
			uid = input("User ID (email): ").strip()
			pw = input("Password: ").strip()
			role = input("Role (student/professor): ").strip()
			try:
				self.auth.register(uid, pw, role)
				print("Registered.")
			except Exception as e:
				print(f"Error: {e}")
		elif c == "2":
			uid = input("User ID: ").strip()
			pw = input("Password: ").strip()
			print("Login ok" if self.auth.login(uid, pw) else "Login failed")
		elif c == "3":
			uid = input("User ID: ").strip()
			pw = input("New Password: ").strip()
			print("Changed" if self.auth.change_password(uid, pw) else "Not found")
		else:
			print("Invalid.")
