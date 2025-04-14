from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)

ssl_args = {
    "ssl": {
        "ca": "/etc/ssl/cert.pem",
    }
}

engine = create_engine(
    DATABASE_URL,
    connect_args=ssl_args,
    echo=True, 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return "✅ Database connected successfully!"
    except Exception as e:
        return f"❌ Connection failed: {e}"

if __name__ == "__main__":
    result = test_connection()
    print(result)
