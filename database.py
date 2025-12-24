from tortoise import Tortoise
import os
from dotenv import load_dotenv

load_dotenv()

# Get Neon DB connection string from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Tortoise ORM requires 'postgres://' not 'postgresql://'
# Convert postgresql:// to postgres:// if needed
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgres://", 1)

# Remove sslmode parameter and add proper SSL config
# asyncpg uses 'ssl' not 'sslmode'
if "?sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?sslmode=")[0]
elif "&sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("&sslmode=")[0]

async def init_db():
    """
    Initialize database connection and generate schemas
    """
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={'models': ['models']},
    )
    await Tortoise.generate_schemas()
    print("Database initialized successfully")

async def close_db():
    """
    Close database connections
    """
    await Tortoise.close_connections()
    print("Database connections closed")