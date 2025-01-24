from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASSWORD

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# import psycopg2
# conn = psycopg2.connect(f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}")
