import os

import aiofiles
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.concurrency import run_in_threadpool

from src.utils import yolo_processing

router = APIRouter()


# Yolo video processing
@router.post("/video/yolo", tags=["Video"])
async def yolo(file: UploadFile = File(...)):
    try:
        async with aiofiles.tempfile.NamedTemporaryFile("wb", delete=False) as temp:
            try:
                contents = await file.read()
                await temp.write(contents)
            except:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='There was an error uploading the file')
            finally:
                await file.close()

        res = await run_in_threadpool(yolo_processing, temp.name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='There was an error processing the file')
    finally:
        os.remove(temp.name)

    return res
