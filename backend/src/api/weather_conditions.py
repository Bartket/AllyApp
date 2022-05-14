from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def weather_conditions() -> dict:
    response = {
        "temperature": 4,
        "air_conditions": 2
    }
    return response
