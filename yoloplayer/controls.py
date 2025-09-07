import cv2

class YOLOPlayer:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise Exception("Could not open video source")
        
        self.paused = False
        self.fullscreen = False
        self.window_name = "YOLOPlayer"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
        self.frame_index = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # how many frames to skip for forward/rewind
        self.skip_frames = int(self.fps)  # ~1 sec skip

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
                cv2.imshow(self.window_name, frame)

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
    # Replace with "video.mp4" or 0 for webcam
    player = YOLOPlayer("yt2.mp4")
    player.run()