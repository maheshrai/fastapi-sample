from contextlib import asynccontextmanager
from fastapi import FastAPI
from db import close_pool
from routers import customers, billing, outages, workorders


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_pool()


app = FastAPI(title="Electric Utility API", lifespan=lifespan)

app.include_router(customers.router)
app.include_router(billing.router)
app.include_router(outages.router)
app.include_router(workorders.router)
