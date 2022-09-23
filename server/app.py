from fastapi import FastAPI
from .database import db
from .api import api_router

app = FastAPI()
app.include_router(api_router)

# before start
@app.on_event("startup")
async def startup():
    await db.connect()


# after stop
@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
