from app.config.database_config import SessionLocal


def get_db():
    """Yield a database session and close it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
