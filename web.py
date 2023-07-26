import uvicorn
from fastapi import FastAPI

from app.db.database import engine
from app.routes import customers, leads
from config import settings

app = FastAPI(
    debug=settings.debug,
    redoc_url='/redoc',
    docs_url='/docs',
)


app.include_router(customers.router)
app.include_router(leads.router)


@app.on_event("shutdown")
def shutdown():
    engine.dispose()


if __name__ == '__main__':
    uvicorn.run(
        'web:app',
        host=settings.service_host,
        port=settings.service_port,
    )
