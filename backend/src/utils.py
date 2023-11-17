import csv
import os
import shutil
import uuid
import zipfile
from io import BytesIO
from pathlib import Path

from fastapi.responses import StreamingResponse


def yolo_processing(file_path: str):
    root_path = Path(__file__).parent.parent
    random_name = str(uuid.uuid4())
    video_path = Path.joinpath(root_path, f"result/video/{random_name}.mp4")
    csv_path = Path.joinpath(root_path, f"result/csv/{random_name}.csv")

    shutil.copy(file_path, video_path)

    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["00:01:12.123", "Stop"])
        writer.writerow(["00:01:46.567", "Speed limit"])

    filenames = [video_path, csv_path]
    print(filenames)

    return zipfiles(filenames)


def zipfiles(filenames):
    zip_io = BytesIO()
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as temp_zip:
        for fpath in filenames:
            fdir, fname = os.path.split(fpath)
            temp_zip.write(fpath, fname)

    return StreamingResponse(
        iter([zip_io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename=result.zip"}
    )
