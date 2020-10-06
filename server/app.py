from fastapi.applications import FastAPI

from server.api import v1
from server.integrations import openexchangerates
from server.models.repository import db
from server.models.responses import JSONResponse
from server.startup import start_refresh_rates_routine

app = FastAPI()
db.init_app(app)


@app.on_event("startup")
async def startup():
    await start_refresh_rates_routine()


app.include_router(v1.router, prefix="/api/v1")


@app.get("/mirror/openexchangerates.org/api/latest.json")
async def mirror_openexchangerates():
    val = await openexchangerates.raw_request()
    return JSONResponse(val)
