import cv2
import threading

class WebcamEngine:

    def __init__(self, gui):
        self.gui=gui
        self.last_activity="normal"
        self.running=True

    def start(self):
        threading.Thread(target=self.loop,daemon=True).start()

    def loop(self):

        cap=cv2.VideoCapture(0)

        while self.running:

            ret,frame=cap.read()
            if not ret:
                continue

            # só exemplo básico
            h,w,_=frame.shape

            if w<300:
                self.last_activity="sleepy"

            self.gui.show_webcam_frame(frame)