from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
from app.api.router import router as root_router
from app.utils.common import get_current_user

load_dotenv()


app = FastAPI()

security = HTTPBasic()

app.include_router(root_router, prefix="")


# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html(user: str = Depends(get_current_user)):
#     return get_swagger_ui_html(openapi_url=app.openapi_url, title="Custom Docs")
