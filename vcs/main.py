from aiohttp import web
from strawberry import federation
from strawberry.aiohttp.views import GraphQLView
from strawberry.tools import merge_types

import schedule
import student
import version

app = web.Application()

combo_query = merge_types("ComboQuery", (
    schedule.Query, student.Query, version.Query))
schema = federation.Schema(combo_query)

app.router.add_view(
    "/", GraphQLView(schema, graphiql=False))

if __name__ == "__main__":
    web.run_app(app)
