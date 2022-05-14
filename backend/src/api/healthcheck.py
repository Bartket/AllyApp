from fastapi import APIRouter
from loguru import logger

router = APIRouter()


@router.get("/")
def healthcheck() -> dict:
    logger.info("Healthcheck OK")
    logger.error("Healthcheck OK")
    logger.debug("Healthcheck OK")

    return {"Healthcheck": "OK"}
