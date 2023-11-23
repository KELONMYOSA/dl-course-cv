import json
import logging
import math
import tempfile
import uuid
from os import path

import cv2
from aiofiles import os
from ultralytics import YOLO

logging.getLogger("ultralytics").setLevel(logging.ERROR)

model = YOLO("storage/weights/120_epochs.pt")
with open("storage/maps/our_signs_map.json") as json_file:
    signs_map = json.load(json_file)
with open("storage/maps/text_info_mapping.json") as json_file:
    text_info_map = json.load(json_file)
with open("storage/maps/high_priority_mapping.json") as json_file:
    priority_map = json.load(json_file)


def _predict_img(path: str):
    result = model(path, conf=0.5)
    return result[0]


def priority_flag(sign_name: str) -> int:
    if sign_name in priority_map.keys():
        return 1
    else:
        return 0


async def predict_video(input_video_path: str, out_video_path: str, logs_file, per_second: int = 1):
    tmp_dir = tempfile.gettempdir()
    cap = cv2.VideoCapture(input_video_path)

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    video_shape = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out_video_frames = []

    frame_count = 0
    frame_interval = math.ceil(video_fps / per_second)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        if frame_count % frame_interval == 0:
            tmp_frame_img = path.join(tmp_dir, f"{uuid.uuid1()!s}.jpg")
            cv2.imwrite(tmp_frame_img, frame)
            res = _predict_img(tmp_frame_img)
            await os.remove(tmp_frame_img)

            detection_count = res.boxes.shape[0]
            for i in range(detection_count):
                cls = int(res.boxes.cls[i].item())
                name = res.names[cls]
                if name in signs_map and name in priority_map and name in text_info_map:
                    await logs_file.write(
                        f"{round(frame_count / video_fps, 1)},{name},{signs_map[name]},"
                        f"{text_info_map[name]},{priority_flag(name)}\n"
                    )

            out_video_frames.append(res.plot())
        else:
            out_video_frames.append(frame)

    cap.release()

    out = cv2.VideoWriter(out_video_path, cv2.VideoWriter_fourcc(*"vp80"), video_fps, video_shape)

    for frame in out_video_frames:
        out.write(frame)
