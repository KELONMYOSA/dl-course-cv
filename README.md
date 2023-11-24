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
