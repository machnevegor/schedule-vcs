from asyncio import gather

from strawberry.dataloader import DataLoader
from utils.config import API_URL

from graphs.student.models import Student
from utils.gql import Query

student_query = Query(
    "query($studentId:OID!){student(studentId:$studentId)"
    "{id firstName lastName classNumber tableLink}}",
    endpoint=API_URL
)


async def load_students(student_ids: list[str]) -> list[Student]:
    tasks = [
        student_query.execute({"studentId": student_id})
        for student_id in student_ids
    ]

    students = [
        Student.parse_dict(response["data"]["student"])
        for response in await gather(*tasks)
    ]

    return students


student_loader = DataLoader(
    load_fn=load_students
)
