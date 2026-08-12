import os

os.environ.setdefault("SECRET_KEY", "test-only-secret-key-with-adequate-length")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://nexusbi:nexusbi@localhost:5432/nexusbi")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("MONGODB_URL", "mongodb://localhost:27017")
