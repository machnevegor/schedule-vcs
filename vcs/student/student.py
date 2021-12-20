import strawberry

from student.loader import student_loader
from student.searcher import find_student
from student.types import Student
from utils.scalars import OID


@strawberry.type
class Query:
    @strawberry.field(description="Get the student's public data using their OID.")
    async def student(self, student_id: OID) -> Student:
        return await student_loader.load(student_id)

    @strawberry.field(description="Find a student using their first and last name.")
    async def find_student(self, search_name: str, accuracy: float = 0.7,
                           limit: int = 10) -> list[Student]:
        assert 0 <= accuracy <= 1, "The accuracy should be between 0 and 1!"
        assert 1 <= limit <= 20, "The limit should be between 1 and 20!"
        matches = await find_student(search_name, accuracy)
        return matches[:limit]
