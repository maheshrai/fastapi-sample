from fastapi import APIRouter
from models.workorder import Crew
import services.workorder_service as svc

router = APIRouter(prefix="/workorders", tags=["Work Orders"])


@router.get("/crews", response_model=list[Crew])
async def list_crews():
    """Get all available crews from Maximo."""
    return await svc.list_crews()
