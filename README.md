# Inventory tracking system

## Functionality (annotated with MoSCoW priority)

### Login (M)

- with email and password

### Add new item (M)

- Specify name, manufacturer, quantity and threshold - only name is required and unique (M)
- Suggest existing items by name to avoid duplication and switch to editing if selected (C)

### List items in my inventory (M)

- Search by name and manufacturer (M)
- Live search suggestions (S)
- Sort by name or quantity (S)
- Filter by manufacturer (select from available options) (C)
- Option to hide items with 0 quantity (S)
- Find items with quantities below threshold (restock needed) (M)

### Edit existing item - change any field (M)

### Quickly change quantity of an item - add or reduce by specified amount (M)

### Register (W) - accounts will be created manually by system administrator

## Technology used

- FastAPI - async web framework with pydantic for validation
- PostgreSQL + SQLAlchemy
- Vue.js for the frontend

## Installing dependencies

`pip install -r requirements.txt`
`cd frontend && npm install`

## Running

Create backend/.env file with SECRET_KEY and DATABASE_URL
`cd frontend && npm run serve`  
`cd backend && uvicorn app.main:app --reload`
