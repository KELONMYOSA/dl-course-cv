## DL Course - CV

### How to start

```
docker compose up -d
```


### Experiments results

model       | epoch num | time | optimizer | lr     | momentum  | box | f1 score
------------|-----------|------|-----------|--------|-----------|-----|---------
yolov8      | 10        | 2.5ч | SGD       | 0.01   | 0.937     | 7.5 | 0.78
yolov8      | 10        | 2.5ч | SGD       | 0.01   | 0.937     | 0.05| 0.57
yolov8      | 70        | 17.5 | SGD       | 0.01   | 0.937     | 7.5 | 0.88
yolov8      | 120       | 30ч  | SGD       | 0.01   | 0.937     | 7.5 | 0.90
faster-rcnn | 2         | 5ч   | SGD       | 0.0005 | 0.9       | -   | 0.53
faster-rcnn | 2         | 5ч   | SGD       | 0.001  | 0.9       | -   | 0.56
faster-rcnn | 4         | 10ч  | SGD       | 0.001  | 0.9       | -   | 0.55
faster-rcnn | 2         | 5ч   | Adam      | 0.001  | 0.9       | -   | 0.00

### Web UI
![Web UI - GIF](assets/web-ui.gif)


### Portability

| Model                                                                                | size<br><sup>(pixels) | mAP<sup>val<br>50-95 | Speed<br><sup>CPU ONNX<br>(ms) | Speed<br><sup>A100 TensorRT<br>(ms) | params<br><sup>(M) | FLOPs<br><sup>(B) |
| ------------------------------------------------------------------------------------ | --------------------- | -------------------- | ------------------------------ | ----------------------------------- | ------------------ | ----------------- |
| [YOLOv8n](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt) | 640                   | 37.3                 | 80.4                           | 0.99                                | 3.2                | 8.7               |
| [YOLOv8s](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt) | 640                   | 44.9                 | 128.4                          | 1.20                                | 11.2               | 28.6              |
| [YOLOv8m](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt) | 640                   | 50.2                 | 234.7                          | 1.83                                | 25.9               | 78.9              |
| [YOLOv8l](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8l.pt) | 640                   | 52.9                 | 375.2                          | 2.39                                | 43.7               | 165.2             |
| [YOLOv8x](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt) | 640                   | 53.9                 | 479.1                          | 3.53                                | 68.2               | 257.8             |

- Inference speed is measured by Ultralytics on Amazon EC2 P4d instance with 96 vCPU and 8 x Nvidia A100.
- Consider we're using 1280p resolution and YOLOv8n as backbone of our solution, even on mobile device CPU we'll get enough framerate to detect all signs in realtime.
