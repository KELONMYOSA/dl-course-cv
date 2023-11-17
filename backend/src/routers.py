from fastapi import APIRouter

from src.utils import yolo_processing

router = APIRouter()


# Yolo video processing
@router.post("/video/yolo", tags=["Video"])
async def yolo():
    return yolo_processing()
