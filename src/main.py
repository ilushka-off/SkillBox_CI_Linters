from fastapi import FastAPI

from SkillBox_CI_Linters import api_router

app = FastAPI(title="Client Parking Swagger", openapi_url="/api/openapi.json", docs_url="/api/swagger", version="1.2.1")

app.include_router(api_router)