from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Student:
	email_address: str
	first_name: str
	last_name: str
	course_id: str
	grade: str
	marks: float

	def key_email(self) -> str:
		return self.email_address.lower()


@dataclass
class Course:
	course_id: str
	course_name: str
	description: str = ""
	credits: Optional[int] = None

	def key_id(self) -> str:
		return self.course_id.upper()


@dataclass
class Professor:
	professor_id: str
	name: str
	rank: str
	course_id: str
	email_address: Optional[str] = None

	def key_id(self) -> str:
		return self.professor_id.lower()


@dataclass
class Grade:
	grade_id: str
	grade: str
	marks_range: str

	def key_id(self) -> str:
		return self.grade_id.upper()


@dataclass
class LoginUser:
	user_id: str
	password_encrypted: str
	role: str

	# password handling occurs via crypto utilities, not here
