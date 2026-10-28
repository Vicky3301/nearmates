from sqlalchemy import text

from app.database import engine


def check_database_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful:", result.scalar_one())


if __name__ == "__main__":
    check_database_connection()