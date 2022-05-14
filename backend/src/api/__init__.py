from fastapi import FastAPI
from api.locations.routes import router as locations_router
from api.routes.routes import router as routes_router
from api.healthcheck import router as healthcheck_router
from api.weather_conditions import router as weather_conditions_router


def init_routers(app: FastAPI) -> None:
    app.include_router(healthcheck_router, prefix="/healthcheck")
    app.include_router(locations_router, prefix="/locations")
    app.include_router(routes_router, prefix="/routes")
    app.include_router(weather_conditions_router, prefix="/weather_conditions")
