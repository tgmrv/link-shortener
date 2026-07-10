from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    BASE_URL: str

def get_settings() -> Settings:
    return Settings(
    DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/postgres",
    BASE_URL = "http://localhost:8000"
    )

settings = get_settings()