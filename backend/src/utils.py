import zipfile
from io import BytesIO

import aiofiles
from aiofiles import os
from fastapi.responses import StreamingResponse
from pytube import YouTube


async def yolo_processing(file_path: str):
    # Video process
    async with aiofiles.tempfile.NamedTemporaryFile("wb", delete=False) as temp_video:
        async with aiofiles.open(file_path, mode="rb") as file:
            contents = await file.read()
            await temp_video.write(contents)

    # CSV process
    async with aiofiles.tempfile.NamedTemporaryFile("w", delete=False) as temp_csv:
        await temp_csv.write("0.56, Stop\n")
        await temp_csv.write("3.23, Speed limit\n")

    zip_result = zipfiles(temp_video.name, temp_csv.name)
    await os.remove(temp_video.name)
    await os.remove(temp_csv.name)

    return zip_result


def zipfiles(f_video: str, f_csv: str):
    zip_io = BytesIO()
    with zipfile.ZipFile(zip_io, mode="w", compression=zipfile.ZIP_DEFLATED) as temp_zip:
        temp_zip.write(f_video, "video.mp4")
        temp_zip.write(f_csv, "data.csv")

    return StreamingResponse(
        iter([zip_io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": "attachment; filename=result.zip"},
    )


async def yt_download_tmp(yt_url: str) -> str:
    yt = YouTube(yt_url)
    video_buffer = BytesIO()
    yt.streams.filter(file_extension="mp4").get_highest_resolution().stream_to_buffer(video_buffer)
    async with aiofiles.tempfile.NamedTemporaryFile("wb", delete=False) as temp:
        await temp.write(video_buffer.getbuffer())

    return temp.name
