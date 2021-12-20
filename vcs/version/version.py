from typing import Optional

import strawberry

from utils.scalars import OID
from version.loader import version_loader
from version.searcher import find_version
from version.types import Version


@strawberry.type
class Query:
    @strawberry.field(description="Get version data using its OID.")
    async def version(self, version_id: OID) -> Version:
        return await version_loader.load(version_id)

    @strawberry.field(description="View all versions of the student's schedule.")
    async def find_version(self, student_id: OID, cursor: Optional[OID] = None,
                           limit: int = 5) -> list[Version]:
        assert 1 <= limit <= 10, "The limit should be between 1 and 10!"
        return await find_version(student_id, cursor, limit)
