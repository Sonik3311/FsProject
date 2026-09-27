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

Требования: Python 3.11+ и запущенный PostgreSQL (см. «Подготовка БД» ниже).

### 1. Подготовка БД (PostgreSQL)

```bash
# создать и запустить контейнер с БД (имя БД — cook_assistant, пароль — postgres)
docker run -d --name cook-db -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=cook_assistant \
  postgres:16-alpine
```
Проверка, что БД доступна:

```bash
pg_isready -h 127.0.0.1 -p 5432
```

### 2. Установка зависимостей и настройка

```bash
cd backend

# создать виртуальное окружение и установить зависимости
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# создать файл настроек из примера
cp .env.example .env
```

Отредактируйте `backend/.env` под вашу БД:

```bash
# строка подключения: postgresql+psycopg://<пользователь>:<пароль>@<хост>:<порт>/<имя_базы>
# для Docker-варианта подойдёт значение по умолчанию
DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5432/cook_assistant
```

### 3. Создание таблиц

Таблицы создаются автоматически при запуске сервера (см. `backend/app/main.py`, событие `startup` → `Base.metadata.create_all`). Отдельных миграций не требуется:

- `ingredients` — ингредиенты
- `dishes` — блюда
- `dish_ingredients` — состав блюда (связующая таблица)
- `wastage` — журнал списаний

Проверить создание таблиц:

```bash
# в отдельном терминале
docker exec -it cook-db psql -U postgres -d cook_assistant -c "\dt"
```

Если нужно сбросить схему (удалит ВСЕ данные):

```bash
docker exec -it cook-db psql -U postgres -d cook_assistant -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

После этого перезапустите сервер — таблицы создадутся заново.

### 4. Запуск сервера

```bash
cd backend
source .venv/bin/activate

# по умолчанию http://127.0.0.1:8000
uvicorn app.main:app --reload
```

Проверка:

- Swagger-документация API: http://127.0.0.1:8000/docs
- Проверка здоровья: http://127.0.0.1:8000/api/health

> Для продакшена вместо автозоздания таблиц лучше использовать миграции Alembic.

### Доступные API-маршруты

#### Ингредиенты `/api/ingredients`

| Метод | Путь | Описание |
|---|---|---|
| GET | `/api/ingredients` | список ингредиентов |
| GET | `/api/ingredients/{id}` | ингредиент по id |
| POST | `/api/ingredients` | создать ингредиент |
| PATCH | `/api/ingredients/{id}` | частично обновить (только переданные поля) |
| DELETE | `/api/ingredients/{id}` | удалить (409, если используется в блюдах/списаниях) |

#### Блюда `/api/dishes`

| Метод | Путь | Описание |
|---|---|---|
| GET | `/api/dishes` | список блюд с себестоимостью и аллергенами |
| GET | `/api/dishes/{id}` | карточка блюда |
| POST | `/api/dishes` | создать блюдо из ингредиентов |
| PATCH | `/api/dishes/{id}` | обновить имя и/или заменить состав |
| DELETE | `/api/dishes/{id}` | удалить (состав удаляется каскадно) |

#### Списания `/api/wastage`

| Метод | Путь | Описание |
|---|---|---|
| GET | `/api/wastage` | журнал списаний |
| GET | `/api/wastage/{id}` | запись списания |
| POST | `/api/wastage` | записать списание (единица берётся из ингредиента) |
| PATCH | `/api/wastage/{id}` | обновить (при смене ингредиента единица пересчитывается) |
| DELETE | `/api/wastage/{id}` | удалить запись |

#### Прочее

| Метод | Путь | Описание |
|---|---|---|
| GET | `/api/allergens/matrix` | матрица аллергенов по меню |
| GET | `/api/health` | проверка здоровья сервера |

Коды ответов: `201` — создано, `204` — удалено, `400` — неверные данные/несуществующая ссылка, `404` — не найдено, `409` — конфликт (дубликат уникального значения или нарушение связей), `422` — ошибка валидации Pydantic.

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
