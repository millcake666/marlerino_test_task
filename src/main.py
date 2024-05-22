from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from utils import include_routers
from config import get_settings


settings = get_settings()
app = FastAPI(title=settings.APP_NAME)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def startup():
    include_routers(app, __file__)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT)
