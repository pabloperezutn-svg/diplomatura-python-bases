import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


Base = declarative_base()

# Variable para elegir la base de datos: "sqlite" o "postgres"
DB_ENGINE = os.getenv("DB_ENGINE", "sqlite")  # Por defecto usa sqlite
SQLITE_CONNECTION = os.getenv("SQLITE_CONNECTION", "sqlite:///./instance/library.db")
POSTGRES_CONNECTION = os.getenv("POSTGRES_CONNECTION")

if DB_ENGINE == "sqlite":
    SQLALCHEMY_DATABASE_URL = f"{SQLITE_CONNECTION}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}  # Solo para SQLite
    )
elif DB_ENGINE == "postgres":
    SQLALCHEMY_DATABASE_URL = f"{POSTGRES_CONNECTION}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    raise ValueError(f"DB_ENGINE '{DB_ENGINE}' no está soportado")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()