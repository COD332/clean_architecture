import click
from uuid import UUID
from app.adapters.db.repositories import user_repo

@click.argument("user_id")
def main(user_id):
    user_id = UUID(user_id)
    user = user_repo.get(user_id)

    if not user:
        print(f"User with id {user_id} not found")
    else:
        print(f"name : {user.name}\nid : {user.id}\n")
