from typing import Any

from attr import dataclass
from fuzzywuzzy.fuzz import token_sort_ratio

from student.types import Student
from utils.env import MONGO_URI, DATABASE_NAME
from utils.mongo import MongoClient


@dataclass
class Match:
    ratio: int
    value: Any


async def find_student(search_name: str, accuracy: float) -> list[Student]:
    matches = []
    async with MongoClient(MONGO_URI) as client:
        student_collection = client[DATABASE_NAME]["students"]

        filters = {"$and": [
            {"classNumber": {"$ne": None}},
            {"tableLink": {"$ne": None}}
        ]}

        async for student in student_collection.find(filters):
            full_name = student["firstName"] + " " + student["lastName"]
            ratio = token_sort_ratio(search_name, full_name)
            if ratio >= accuracy * 100:
                matches.append(Match(ratio, student))

    students = [
        Student.parse_dict(match.value) for match in sorted(
            matches, key=lambda match: match.ratio, reverse=True)
    ]

    return students
