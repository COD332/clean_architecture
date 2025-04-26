# clean_architecture

## Run Tests

```bash
python -m app.adapters.commands.manage get_user_by_id 3fa85f64-5717-4562-b3fc-2c963f66afa6
```
---
## Run FastAPI

```bash
uvicorn app.adapters.api.rest.fastapi_app.main:app --reload 
```
---
## Run Flask

```bash
export FLASK_APP=app.adapters.api.rest.flask_app.main
export PYTHONPATH=/home/ali/Dev/Personal/CA/final/book_lending_system 
flask run -p 8000
```
