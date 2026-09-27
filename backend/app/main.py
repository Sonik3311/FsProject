from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from .config import settings
from .database import Base, engine
from .routes import allergens, dishes, ingredients, wastage

app = FastAPI(title=settings.app_name)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(_: Request, __: IntegrityError) -> JSONResponse:
    """Нарушение ограничений БД (уникальность, внешние ключи) → HTTP 409."""
    return JSONResponse(
        status_code=409,
        content={"detail": "Конфликт данных: запись с такими значениями уже существует"},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingredients.router, prefix="/api")
app.include_router(dishes.router, prefix="/api")
app.include_router(wastage.router, prefix="/api")
app.include_router(allergens.router, prefix="/api")


@app.on_event("startup")
def create_tables() -> None:
    """Создаёт таблицы при запуске. Для продакшена используйте миграции (Alembic)."""
    Base.metadata.create_all(bind=engine)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}