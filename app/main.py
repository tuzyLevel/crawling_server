from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv
from app.api.router import router as root_router
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.utils.crawling import crawl_job

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler.add_job(
        crawl_job,
        trigger=CronTrigger(hour=23, minute=39, second=0)
    )
    scheduler.start()
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
scheduler = AsyncIOScheduler()


security = HTTPBasic()

app.include_router(root_router, prefix="")


# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html(user: str = Depends(get_current_user)):
#     return get_swagger_ui_html(openapi_url=app.openapi_url, title="Custom Docs")
