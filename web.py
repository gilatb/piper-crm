import time
import uuid

import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger
from httpx import Request

from app.db.database import engine
from app.routes import customers, leads
from config import settings

app = FastAPI(
    debug=settings.debug,
    redoc_url='/redoc',
    docs_url='/docs',
)


app.include_router(leads.router)
app.include_router(customers.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = uuid.uuid4().hex[:6]
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(
        f"rid={idem} "
        f"completed_in={formatted_process_time}ms "
        f"status_code={response.status_code}"
    )

    return response


@app.on_event("shutdown")
def shutdown():
    engine.dispose()


if __name__ == '__main__':
    uvicorn.run(
        'web:app',
        host=settings.service_host,
        port=settings.service_port,
        reload=settings.autoreload,
    )
