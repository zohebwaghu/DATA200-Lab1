from checkmygrade.services import StudentService
from checkmygrade.models import Student
from checkmygrade.storage import CsvPaths, ensure_data_dir
import os, time

ensure_data_dir()
base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
uniq = str(time.time_ns())
CsvPaths.students = os.path.join(base_dir, f"diag_students_{uniq}.csv")

svc = StudentService()
print("initial index size:", len(svc._index))
try:
	svc.add(Student("x@example.edu", "A", "B", "DATA200", "A", 95.0))
	print("added 1")
	svc.add(Student("y@example.edu", "A", "B", "DATA200", "A", 90.0))
	print("added 2")
except Exception as e:
	print("error:", e)
