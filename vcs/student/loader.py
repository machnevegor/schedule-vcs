from pymongo import DESCENDING
from strawberry.dataloader import DataLoader

from student.types import Student
from utils.config import MONGO_URI, DATABASE_NAME
from utils.mongo import MongoClient
from utils.scalars import OID


async def load_students(student_ids: list[OID]) -> list[Student | Exception]:
    students = []
    async with MongoClient(MONGO_URI) as client:
        student_collection = client[DATABASE_NAME]["students"]

        for student_id in student_ids:
            student = await student_collection.find_one(
                {"_id": student_id}, sort=[("_id", DESCENDING)])

            if student:
                students.append(
                    Student.parse_dict(student))
            else:
                students.append(
                    Exception("No student with this OID!"))

    return students


student_loader = DataLoader(
    load_fn=load_students
)
