from utils.config import API_URL

from graphs.student.models import Student
from utils.gql import Query

student_query = Query(
    "query($searchName:String!){findStudent(searchName:$searchName)"
    "{id firstName lastName classNumber tableLink}}",
    endpoint=API_URL
)


async def find_student(search_name: str) -> list[Student]:
    response = await student_query.execute(
        {"searchName": search_name})

    matches = [
        Student.parse_dict(student)
        for student in response["data"]["findStudent"]
    ]

    return matches
