from fastapi import FastAPI

from .database import Base
from .database import engine

from .routes.users import router as users_router

# Import models so SQLAlchemy knows about them.
from .models.user import User
from .models.email_job import EmailJob
from .models.outbox import OutboxEvent


app = FastAPI(
    title="Email Queue System",
    description="Asynchronous email queue using Neon PostgreSQL, RabbitMQ and S3",
    version="2.0.0",
)


@app.on_event("startup")
def startup():

    Base.metadata.create_all(
        bind=engine
    )


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


app.include_router(users_router)