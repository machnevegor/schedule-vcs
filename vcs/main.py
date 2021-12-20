from aiohttp import web
from strawberry import federation
from strawberry.aiohttp.views import GraphQLView
from strawberry.tools import merge_types

import schedule
import student
import version

app = web.Application()

schema = federation.Schema(
    query=merge_types("ComboQuery", (
        schedule.Query, student.Query, version.Query)))

app.router.add_view(
    "/", GraphQLView(schema, graphiql=False))

web.run_app(app)
