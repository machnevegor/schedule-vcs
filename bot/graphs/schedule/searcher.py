from graphs.schedule.models import Schedule
from utils.config import API_URL
from utils.gql import Query

schedule_query = Query(
    "query($studentId:OID!){findSchedule(studentId:$studentId)"
    "{id days{name lessons{number name group teacher room}}}}",
    endpoint=API_URL
)


async def find_schedule(student_id: str) -> list[Schedule]:
    response = await schedule_query.execute(
        {"studentId": student_id})

    schedule = Schedule.parse_dict(
        response["data"]["findSchedule"])

    return schedule
