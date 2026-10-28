from app.database import SessionLocal
from app.services.catalogue import seed_catalogue


def main():
    with SessionLocal() as db:
        seed_catalogue(db)

    print("Language and interest catalogues seeded successfully.")


if __name__ == "__main__":
    main()