import os
import uvicorn
import sys
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
import logging
from container import Container
from starlette.middleware.gzip import GZipMiddleware
from routers import api_router
from config import Config


def create_app(
) -> FastAPI:
    container = Container()
    container.init_resources()
    container.wire(modules=[
        sys.modules[__name__],
        sys.modules['routers.api'],
        # sys.modules['connectors.minio']
    ],
        packages=["routers.api", "connectors.minio"],
    )
    try:

        # App
        app = FastAPI()

        # middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # fix problem to ignore that exception if the request is disconnected
        # https://github.com/encode/starlette/issues/1634#issuecomment-1124806406
        app.add_middleware(GZipMiddleware)

        # Config
        app.state.Config = Config()

        # Routers
        app.include_router(api_router)

        # minio check buckets if exist

        logger = logging.getLogger(__name__)

        @app.on_event("startup")
        async def on_startup() -> None:
            logger.info("Приложение запущено")

        @app.on_event("shutdown")
        async def on_shutdown() -> None:
            logger.info("Приложение выключено")

        return app
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception(f"Service crashed vs Exception: {e}")


if __name__ == "__main__":
    app = create_app()

    uvicorn.run(
        app,
        host=os.environ.get("SERVICE_HOST", "0.0.0.0"),
        port=int(os.environ.get("SERVICE_ENDPOINT_PORT", 8081)),
        workers=int(os.environ.get("SERVICE_UVICORN_WORKERS", 1))
    )
