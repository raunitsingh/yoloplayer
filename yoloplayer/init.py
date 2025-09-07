from .controls import YOLOPlayer as ControlsPlayer
from .yolo import YOLOPlayer as YOLOImpl

class YOLOPlayer:
    def __new__(cls, source=0, use_yolo=False, model_path="yolov8n.pt"):
        if use_yolo:
            return YOLOImpl(source, model_path=model_path)
        return ControlsPlayer(source)


