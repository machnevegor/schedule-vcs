from typing import Any

from aiohttp import ClientSession
from attr import dataclass


@dataclass
class Query:
    query: str
    endpoint: str

    async def execute(self, variables: dict[str, Any]) -> dict:
        async with ClientSession() as session:
            async with session.post(self.endpoint, json=dict(
                    query=self.query, variables=variables)) as resp:
                return await resp.json()
