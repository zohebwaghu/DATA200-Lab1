import os
import random
import string
import time
import unittest

from checkmygrade.models import Student, Course, Professor, Grade
from checkmygrade.services import StudentService, CourseService, ProfessorService, GradeService, AuthService
from checkmygrade.storage import CsvPaths, ensure_data_dir
from checkmygrade.crypto import encrypt_password, decrypt_password


class CheckMyGradeTests(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		ensure_data_dir()

	@classmethod
	def tearDownClass(cls):
		pass

	def setUp(self):
		# assign unique file paths per test run to ensure isolation
		base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
		uniq = str(time.time_ns())
		CsvPaths.students = os.path.join(base_dir, f"test_students_{uniq}.csv")
		CsvPaths.courses = os.path.join(base_dir, f"test_courses_{uniq}.csv")
		CsvPaths.professors = os.path.join(base_dir, f"test_professors_{uniq}.csv")
		CsvPaths.grades = os.path.join(base_dir, f"test_grades_{uniq}.csv")
		CsvPaths.logins = os.path.join(base_dir, f"test_logins_{uniq}.csv")
		self.students = StudentService()
		self.courses = CourseService()
		self.profs = ProfessorService()
		self.grades = GradeService()
		self.auth = AuthService()

	def test_encryption_roundtrip(self):
		pw = "Welcome12#_"
		enc = encrypt_password(pw)
		self.assertNotEqual(enc, pw)
		self.assertEqual(decrypt_password(enc), pw)

	def test_course_crud(self):
		c = Course(course_id="DATA200", course_name="Data Science", description="Intro", credits=3)
		self.courses.add(c)
		self.assertEqual(len(self.courses.all()), 1)
		self.assertTrue(self.courses.update("DATA200", description="Updated"))
		self.assertTrue(self.courses.delete("DATA200"))

	def test_professor_crud(self):
		p = Professor(professor_id="micheal@mycsu.edu", name="Micheal John", rank="Senior Professor", course_id="DATA200")
		self.profs.add(p)
		self.assertTrue(self.profs.update(p.professor_id, rank="Professor"))
		self.assertTrue(self.profs.delete(p.professor_id))

	def test_student_crud_and_search_sort(self):
		# add 1000 records
		n = 1000
		for i in range(n):
			email = f"student{i}@example.edu"
			self.students.add(Student(email, "First", "Last", "DATA200", "A", float(i % 101)))
		# search timing
		start = time.perf_counter()
		res = self.students.find(lambda s: s.email_address == "student500@example.edu")
		elapsed = time.perf_counter() - start
		print(f"Search among {n} took {elapsed:.6f}s")
		self.assertEqual(len(res), 1)
		# sort timing
		sorted_rows, sort_elapsed = self.students.sort(lambda s: s.marks, reverse=True)
		print(f"Sort {n} records took {sort_elapsed:.6f}s")
		self.assertEqual(len(sorted_rows), n)
		# delete & update
		self.assertTrue(self.students.update("student0@example.edu", marks=99.9))
		self.assertTrue(self.students.delete("student1@example.edu"))

	def test_stats(self):
		# ensure data exists for course
		self.students.add(Student("stats1@example.edu", "A", "B", "DATA200", "A", 90.0))
		self.students.add(Student("stats2@example.edu", "C", "D", "DATA200", "A", 80.0))
		avg, med = self.students.stats_for_course("DATA200")
		self.assertIsNotNone(avg)
		self.assertIsNotNone(med)
		self.assertTrue(80.0 <= med <= 90.0)

	def test_auth(self):
		uid = "micheal@mycsu.edu"
		self.auth.register(uid, "Welcome12#_", "professor")
		self.assertTrue(self.auth.login(uid, "Welcome12#_"))
		self.assertTrue(self.auth.change_password(uid, "NewPass!234"))
		self.assertTrue(self.auth.login(uid, "NewPass!234"))


if __name__ == "__main__":
	unittest.main(verbosity=2)
