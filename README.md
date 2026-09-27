# Ассистент повара: калькулятор себестоиомсти блюд, матрица аллергенов, печать этикеток, учёт списаний.

## Основные пользовательские сценарии:
1. Повар создаёт/редактирует рецепт блюда из ингредиентов и автоматически видит его себестоимость.
2. Ввод закупочных цен на ингредиенты → пересчёт себестоимости блюд.
3. Отметка аллергенов для ингредиента/блюда → формирование матрицы аллергенов по всему меню.
4. Печать этикетки для готового блюда (название, состав/аллергены, дата, себестоимость).
5. Учёт списания продуктов (порча, брак, истечение срока) с фиксацией причины и количества.

## Необходимые экраны:
- Список блюд (меню) + карточка блюда/рецепта
- Справочник ингредиентов (с ценами и аллергенами)
- Экран матрицы аллергенов
- Экран печати/просмотра этикеток
- Журнал списаний + форма списания

## Технологии

- Frontend (`frontend/`): React 19, TypeScript, Vite, Material UI (MUI 9), react-router-dom.
- Backend (`backend/`): Python, FastAPI, SQLAlchemy 2, PostgreSQL, Pydantic.

## Структура проекта

```
Project/
├── frontend/          # React-приложение (клиент)
│   ├── src/
│   │   ├── pages/     # экраны (меню, ингредиенты, аллергены, этикетки, списания)
│   │   ├── components/ # переиспользуемые компоненты
│   │   ├── types/     # типы данных
│   │   └── data/      # mock-данные (пока фронтенд работает без сервера)
│   └── package.json
└── backend/           # FastAPI-приложение (API + БД)
    ├── app/
    │   ├── main.py        # точка входа, CORS, подключение маршрутов
    │   ├── config.py      # настройки из переменных окружения / .env
    │   ├── database.py    # движок SQLAlchemy, сессии, зависимость get_db
    │   ├── models.py      # SQLAlchemy-модели (Ingredient, Dish, WastageEntry)
    │   ├── schemas.py     # Pydantic-схемы валидации запросов/ответов
    │   ├── crud.py        # операции с данными и бизнес-логика (себестоимость, матрица аллергенов)
    │   └── routes/        # маршруты API: ingredients, dishes, wastage, allergens
    ├── requirements.txt
    └── .env.example   # пример настроек без секретов (скопируйте в .env)
```

## Запуск frontend

Требования: установленный [Node.js](https://nodejs.org/) (LTS).

```bash
cd frontend

# 1. Установить зависимости (только при первом запуске или после изменений в package.json)
npm install

# 2. Запустить сервер разработки (по умолчанию http://localhost:5173)
npm run dev
```

Открыть адрес из вывода команды в браузере. Изменения в коде применяются автоматически (HMR).

Полезные команды:

```bash
npm run build    # собрать production-версию (в папку dist/)
npm run preview  # показать собранную версию локально
npm run lint     # проверить код линтером (oxlint)
```

## Запуск backend

Требования: Python 3.11+, запущенный PostgreSQL (например, через Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=cook_assistant postgres:16-alpine`).

```bash
cd backend

# 1. Создать виртуальное окружение и установить зависимости
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Настроить подключение к БД
cp .env.example .env
#    отредактируйте .env: укажите DATABASE_URL, порт и т.д.

# 3. Запустить сервер (по умолчанию http://127.0.0.1:8000)
uvicorn app.main:app --reload
```

Проверка:

- Swagger-документация API: http://127.0.0.1:8000/docs
- Проверка здоровья: http://127.0.0.1:8000/api/health

Таблицы в БД создаются автоматически при старте (для продакшена лучше подключить миграции Alembic).

### Доступные API-маршруты

| Метод | Путь | Описание |
|---|---|---|
| GET | `/api/ingredients` | список ингредиентов |
| POST | `/api/ingredients` | создать ингредиент |
| GET | `/api/dishes` | список блюд с себестоимостью и аллергенами |
| POST | `/api/dishes` | создать блюдо из ингредиентов |
| GET | `/api/dishes/{id}` | карточка блюда |
| GET | `/api/allergens/matrix` | матрица аллергенов по меню |
| GET | `/api/wastage` | журнал списаний |
| POST | `/api/wastage` | записать списание |

Все параметры подключения к БД и серверу задаются в `.env` (см. `.env.example` — там только примеры без секретов; сам файл `.env` в git не попадает).

## Сущности и связи (схема БД)

Проект состоит из четырёх сущностей. Связи между ними:

```
ingredients 1 ──── * dish_ingredients * ──── 1 dishes
    │                                              │
    │ 1                                             │
    │                                              │
    ▼                                              │
 wastage                                          (блюдо из ингредиентов)
```

- **Ingredient** (ингредиент) — справочник продуктов с ценами и аллергенами.
- **Dish** (блюдо) — позиция меню.
- **DishIngredient** (состав блюда) — связующая таблица «многие ко многим» между блюдами и ингредиентами с количеством в составе.
- **WastageEntry** (списание) — запись о списании продукта (порча, брак, истечение срока).

### ingredients — справочник ингредиентов

| Поле | Тип | Ограничения |
|---|---|---|
| `id` | integer (serial) | **PRIMARY KEY** |
| `name` | varchar(100) | NOT NULL, **UNIQUE** (`uq_ingredient_name`) |
| `unit` | varchar(10) | NOT NULL (г, шт, л) |
| `price_per_unit` | float | NOT NULL (цена за единицу) |
| `allergens` | varchar[] | массив строк (например, `['глютен', 'молоко']`) |

Связи: 1 → * `dish_ingredients` (ингредиент входит во многие блюда), 1 → * `wastage` (по ингредиенту ведётся много списаний).

### dishes — блюда (меню)

| Поле | Тип | Ограничения |
|---|---|---|
| `id` | integer (serial) | **PRIMARY KEY** |
| `name` | varchar(100) | NOT NULL, **UNIQUE** (`uq_dish_name`) |

Связи: 1 → * `dish_ingredients` (у блюда много позиций состава, при удалении блюда состав удаляется — `ON DELETE CASCADE`).

### dish_ingredients — состав блюда (связующая таблица)

| Поле | Тип | Ограничения |
|---|---|---|
| `id` | integer (serial) | **PRIMARY KEY** |
| `dish_id` | integer | NOT NULL, **FOREIGN KEY** → `dishes.id` (`ON DELETE CASCADE`) |
| `ingredient_id` | integer | NOT NULL, **FOREIGN KEY** → `ingredients.id` |
| `qty` | float | NOT NULL (количество ингредиента в блюде) |

Дополнительно: **UNIQUE** (`dish_id`, `ingredient_id`) — ингредиент не может быть указан в блюде дважды.

Связи: * → 1 `dishes`, * → 1 `ingredients`. Обеспечивает связь «многие ко многим» между блюдом и ингредиентом.

### wastage — журнал списаний

| Поле | Тип | Ограничения |
|---|---|---|
| `id` | integer (serial) | **PRIMARY KEY** |
| `ingredient_id` | integer | NOT NULL, **FOREIGN KEY** → `ingredients.id` |
| `qty` | float | NOT NULL (списанное количество) |
| `unit` | varchar(10) | NOT NULL (единица на момент списания) |
| `reason` | varchar(200) | NOT NULL (причина: порча, брак, истечение срока) |
| `date` | date | NOT NULL (дата списания) |

Связи: * → 1 `ingredients`.

Модели таблиц — в `backend/app/models.py`, схемы валидации — в `backend/app/schemas.py`, бизнес-логика (расчёт себестоимости, матрица аллергенов) — в `backend/app/crud.py`.
