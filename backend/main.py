from os import getenv

import uvicorn
from fastapi import FastAPI

from app.config.database_config import init_db
from app.routers import daily_stats_router, newcast_router, upload_router

stage = getenv("STAGE", "dev")
app = FastAPI()
init_db()
app.include_router(upload_router.router)
app.include_router(newcast_router.router)
app.include_router(daily_stats_router.router)

if __name__ == "__main__":
    if "prod" in stage:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
