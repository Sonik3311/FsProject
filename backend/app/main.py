from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from .config import settings
from .crud import ConflictError
from .database import Base, engine
from .routes import allergens, dishes, ingredients, wastage

app = FastAPI(title=settings.app_name)

_VALIDATION_MESSAGES: dict[str, str] = {
    "missing": "обязательное поле",
    "string_too_short": "слишком короткое",
    "string_too_long": "слишком длинное",
    "greater_than": "должно быть больше {gt}",
    "greater_than_equal": "должно быть не меньше {ge}",
    "less_than": "должно быть меньше {lt}",
    "int_parsing": "должно быть целым числом",
    "float_parsing": "должно быть числом",
    "finite_number": "должно быть конечным числом",
    "date_parsing": "некорректная дата, формат ГГГГ-ММ-ДД",
    "date_from_datetime_parsing": "некорректная дата, формат ГГГГ-ММ-ДД",
    "literal_error": "недопустимое значение",
    "model_attributes_type": "должно быть объектом",
    "list_type": "должно быть списком",
}


def _localize_validation_error(error: dict) -> str:
    error_type = error.get("type", "")
    template = _VALIDATION_MESSAGES.get(error_type)
    if template is None:
        return error.get("msg", "некорректное значение")
    ctx = error.get("ctx") or {}
    return template.format(**ctx)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    """Ошибки валидации Pydantic → HTTP 422 с понятными русскими сообщениями."""
    errors = []
    for err in exc.errors():
        path = ".".join(str(loc) for loc in err["loc"] if loc not in ("body", "query", "path"))
        errors.append({"field": path or "body", "message": _localize_validation_error(err)})
    return JSONResponse(status_code=422, content={"detail": errors})


@app.exception_handler(IntegrityError)
async def integrity_error_handler(_: Request, __: IntegrityError) -> JSONResponse:
    """Нарушение ограничений БД (уникальность, внешние ключи) → HTTP 409."""
    return JSONResponse(
        status_code=409,
        content={"detail": "Конфликт данных: запись с такими значениями уже существует"},
    )


@app.exception_handler(ConflictError)
async def conflict_error_handler(_: Request, exc: ConflictError) -> JSONResponse:
    """Бизнес-конфликт связей (например, удаление используемого ингредиента) → HTTP 409."""
    return JSONResponse(status_code=409, content={"detail": str(exc)})

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