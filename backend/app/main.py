from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.main import api_router
from app.core.config import settings

from dotenv import load_dotenv

load_dotenv()

def custom_generate_unique_id(route: APIRoute) -> str:
    tag = route.tags[0] if route.tags else "default"
    return f"{tag}-{route.name}"

app = FastAPI(
    title="AI HOME DESIGN GENERATOR",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/", tags=["home"])
async def home_route():
    return JSONResponse(content={"message": "AI HOME DESIGN GENERATOR: v0.0.1"})


app.include_router(api_router, prefix=settings.API_V1_STR)
