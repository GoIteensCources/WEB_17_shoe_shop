import dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


dotenv.load_dotenv()


class DatabaseConfig:
    DATABASE_NAME = os.getenv("DATABASE_NAME", "shoe_store")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    
    def uri_postgres(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@localhost:5433/{self.DATABASE_NAME}"
    
    def uri_sqlite(self):
        return f"sqlite:///{self.DATABASE_NAME}.db"
    
    
config = DatabaseConfig()


# Налаштування бази даних Postgres
engine = create_engine(config.uri_postgres(), echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    def create_db(self):
        self.metadata.create_all(engine)

    def drop_db(self):
        self.metadata.drop_all(engine)
