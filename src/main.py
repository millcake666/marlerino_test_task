from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database import Base, engine
from utils import include_routers
from config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    include_routers(app, __file__)
    yield


settings = get_settings()
app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    import uvicorn
    print(settings.HOST)
    uvicorn.run("main:app", host=settings.HOST, port=int(settings.PORT))
