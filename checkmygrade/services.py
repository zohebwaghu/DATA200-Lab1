from __future__ import annotations

import statistics
import time
from dataclasses import asdict
from typing import Callable, Iterable, List, Optional, Tuple

from .models import Student, Course, Professor, Grade, LoginUser
from .storage import StudentRepo, CourseRepo, ProfessorRepo, GradeRepo, LoginRepo
from .crypto import encrypt_password, decrypt_password


class StudentService:
	def __init__(self, repo: Optional[StudentRepo] = None):
		self.repo = repo or StudentRepo()
		self._cache = self.repo.load_all()
		self._index = {s.key_email(): i for i, s in enumerate(self._cache)}

	def _persist(self) -> None:
		self.repo.save_all(self._cache)

	def add(self, student: Student) -> None:
		key = student.key_email()
		if not student.email_address or key in self._index:
			raise ValueError("email must be unique and not null")
		self._cache.append(student)
		self._index[key] = len(self._cache) - 1
		self._persist()

	def delete(self, email_address: str) -> bool:
		key = email_address.lower()
		idx = self._index.get(key)
		if idx is None:
			return False
		self._cache.pop(idx)
		self._index = {s.key_email(): i for i, s in enumerate(self._cache)}
		self._persist()
		return True

	def update(self, email_address: str, **fields) -> bool:
		key = email_address.lower()
		idx = self._index.get(key)
		if idx is None:
			return False
		s = self._cache[idx]
		for k, v in fields.items():
			if hasattr(s, k):
				setattr(s, k, v)
		self._cache[idx] = s
		self._persist()
		return True

	def find(self, predicate: Callable[[Student], bool]) -> List[Student]:
		start = time.perf_counter()
		results = [s for s in self._cache if predicate(s)]
		elapsed = time.perf_counter() - start
		return results  # timing printed by caller if needed

	def find_by_email(self, email_address: str) -> Optional[Student]:
		return next((s for s in self._cache if s.key_email() == email_address.lower()), None)

	def sort(self, key: Callable[[Student], object], reverse: bool = False) -> Tuple[List[Student], float]:
		start = time.perf_counter()
		result = sorted(self._cache, key=key, reverse=reverse)
		elapsed = time.perf_counter() - start
		return result, elapsed

	def stats_for_course(self, course_id: str) -> Tuple[Optional[float], Optional[float]]:
		marks = [s.marks for s in self._cache if s.course_id.upper() == course_id.upper()]
		if not marks:
			return None, None
		avg = sum(marks) / len(marks)
		med = statistics.median(marks)
		return avg, med

	def report_by_student(self) -> List[dict]:
		return [asdict(s) for s in self._cache]

	def report_by_course(self, course_id: Optional[str] = None) -> List[dict]:
		rows = [s for s in self._cache if not course_id or s.course_id.upper() == course_id.upper()]
		return [asdict(s) for s in rows]

	def report_by_professor(self, professor_course_ids: Iterable[str]) -> List[dict]:
		course_set = {c.upper() for c in professor_course_ids}
		rows = [s for s in self._cache if s.course_id.upper() in course_set]
		return [asdict(s) for s in rows]


class CourseService:
	def __init__(self, repo: Optional[CourseRepo] = None):
		self.repo = repo or CourseRepo()
		self._cache = self.repo.load_all()
		self._index = {c.key_id(): i for i, c in enumerate(self._cache)}

	def _persist(self) -> None:
		self.repo.save_all(self._cache)

	def add(self, course: Course) -> None:
		key = course.key_id()
		if not course.course_id or key in self._index:
			raise ValueError("course_id must be unique and not null")
		self._cache.append(course)
		self._index[key] = len(self._cache) - 1
		self._persist()

	def delete(self, course_id: str) -> bool:
		key = course_id.upper()
		idx = self._index.get(key)
		if idx is None:
			return False
		self._cache.pop(idx)
		self._index = {c.key_id(): i for i, c in enumerate(self._cache)}
		self._persist()
		return True

	def update(self, course_id: str, **fields) -> bool:
		key = course_id.upper()
		idx = self._index.get(key)
		if idx is None:
			return False
		c = self._cache[idx]
		for k, v in fields.items():
			if hasattr(c, k):
				setattr(c, k, v)
		self._cache[idx] = c
		self._persist()
		return True

	def all(self) -> List[Course]:
		return list(self._cache)


class ProfessorService:
	def __init__(self, repo: Optional[ProfessorRepo] = None):
		self.repo = repo or ProfessorRepo()
		self._cache = self.repo.load_all()
		self._index = {p.key_id(): i for i, p in enumerate(self._cache)}

	def _persist(self) -> None:
		self.repo.save_all(self._cache)

	def add(self, prof: Professor) -> None:
		key = prof.key_id()
		if not prof.professor_id or key in self._index:
			raise ValueError("professor_id must be unique and not null")
		self._cache.append(prof)
		self._index[key] = len(self._cache) - 1
		self._persist()

	def delete(self, professor_id: str) -> bool:
		key = professor_id.lower()
		idx = self._index.get(key)
		if idx is None:
			return False
		self._cache.pop(idx)
		self._index = {p.key_id(): i for i, p in enumerate(self._cache)}
		self._persist()
		return True

	def update(self, professor_id: str, **fields) -> bool:
		key = professor_id.lower()
		idx = self._index.get(key)
		if idx is None:
			return False
		p = self._cache[idx]
		for k, v in fields.items():
			if hasattr(p, k):
				setattr(p, k, v)
		self._cache[idx] = p
		self._persist()
		return True

	def courses_for_professor(self, professor_id: str) -> List[str]:
		return [p.course_id for p in self._cache if p.professor_id.lower() == professor_id.lower()]


class GradeService:
	def __init__(self, repo: Optional[GradeRepo] = None):
		self.repo = repo or GradeRepo()
		self._cache = self.repo.load_all()
		self._index = {g.key_id(): i for i, g in enumerate(self._cache)}

	def _persist(self) -> None:
		self.repo.save_all(self._cache)

	def add(self, grade: Grade) -> None:
		key = grade.key_id()
		if not grade.grade_id or key in self._index:
			raise ValueError("grade_id must be unique and not null")
		self._cache.append(grade)
		self._index[key] = len(self._cache) - 1
		self._persist()

	def delete(self, grade_id: str) -> bool:
		key = grade_id.upper()
		idx = self._index.get(key)
		if idx is None:
			return False
		self._cache.pop(idx)
		self._index = {g.key_id(): i for i, g in enumerate(self._cache)}
		self._persist()
		return True

	def update(self, grade_id: str, **fields) -> bool:
		key = grade_id.upper()
		idx = self._index.get(key)
		if idx is None:
			return False
		g = self._cache[idx]
		for k, v in fields.items():
			if hasattr(g, k):
				setattr(g, k, v)
		self._cache[idx] = g
		self._persist()
		return True


class AuthService:
	def __init__(self, repo: Optional[LoginRepo] = None):
		self.repo = repo or LoginRepo()
		self._cache = self.repo.load_all()
		self._index = {u.user_id.lower(): i for i, u in enumerate(self._cache)}

	def _persist(self) -> None:
		self.repo.save_all(self._cache)

	def register(self, user_id: str, password_plain: str, role: str) -> None:
		if not user_id or user_id.lower() in self._index:
			raise ValueError("user_id must be unique and not null")
		enc = encrypt_password(password_plain)
		self._cache.append(LoginUser(user_id=user_id, password_encrypted=enc, role=role))
		self._index[user_id.lower()] = len(self._cache) - 1
		self._persist()

	def login(self, user_id: str, password_plain: str) -> bool:
		idx = self._index.get(user_id.lower())
		if idx is None:
			return False
		u = self._cache[idx]
		return decrypt_password(u.password_encrypted) == password_plain

	def change_password(self, user_id: str, new_password_plain: str) -> bool:
		idx = self._index.get(user_id.lower())
		if idx is None:
			return False
		u = self._cache[idx]
		u.password_encrypted = encrypt_password(new_password_plain)
		self._cache[idx] = u
		self._persist()
		return True
