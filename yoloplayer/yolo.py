import cv2
from ultralytics import YOLO

class YOLOPlayer:
    def __init__(self, source=0, model_path="yolov8n.pt"):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise Exception("Could not open video source")
        
        # Player state
        self.paused = False
        self.fullscreen = False
        self.window_name = "YOLOPlayer"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

        # Video properties
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
        self.frame_index = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.skip_frames = int(self.fps)  # ~1 second skip

        # Load YOLO model
        self.model = YOLO(model_path)

    def toggle_fullscreen(self):
        if self.fullscreen:
            cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
            self.fullscreen = False
        else:
            cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            self.fullscreen = True

    def seek(self, new_index):
        """Jump to a specific frame safely."""
        new_index = max(0, min(new_index, self.total_frames - 1))
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_index)
        self.frame_index = new_index

    def run(self):
        delay = int(1000 / self.fps)  # ms per frame

        while True:
            if not self.paused:
                ret, frame = self.cap.read()
                if not ret:
                    print("End of video or cannot fetch frame")
                    break

                self.frame_index = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

                # Run YOLO detection
                results = self.model(frame, verbose=False)

                # Draw bounding boxes for humans only (class 0 = person)
                for r in results:
                    for box in r.boxes:
                        cls = int(box.cls[0])
                        if cls == 0:  # human only
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            conf = float(box.conf[0])
                            label = f"Human {conf:.2f}"
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(frame, label, (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Show annotated frame
                cv2.imshow(self.window_name, frame)

            # Handle keys
            key = cv2.waitKey(delay if not self.paused else 100) & 0xFF
            if key == ord('q'):  # Quit
                break
            elif key == ord(' '):  # Pause / Play
                self.paused = not self.paused
            elif key == ord('f'):  # Fullscreen toggle
                self.toggle_fullscreen()
            elif key == 81:  # Left Arrow ←
                self.seek(self.frame_index - self.skip_frames)
            elif key == 83:  # Right Arrow →
                self.seek(self.frame_index + self.skip_frames)

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Replace with your video file or 0 for webcam
    player = YOLOPlayer("video.mp4", model_path="yolov8n.pt")
    player.run()