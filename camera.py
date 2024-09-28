import cv2
import os
import mmpose
from mmpose.apis import MMPoseInferencer

from frame_processor import FrameProcessor

class VideoCamera(object):
    FRAME_THRESHOLD = 5

    def __init__(self):
        os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'
        self.video = cv2.VideoCapture(cv2.CAP_V4L2)
        self.frame_processor = FrameProcessor(self.set_points)
        self.frame_counter = 0
        self.points = None

    def set_points(self):
        print("callback triggered")

    def __del__(self):
        self.video.release()

    def paint_points_on_frame(self, frame):
        if self.points is None:
            print("points empty")
            return

        radius = 5
        color = (0, 0, 255)
        thickness = 5

        for x, y, color in self.points:
            frame = cv2.circle(frame, (x, y), radius, color, thickness)

    def get_frame(self):
        ret, frame = self.video.read()
        frame = cv2.flip(frame, 1)
        self.frame_counter = self.frame_counter + 1
        if self.frame_counter == self.FRAME_THRESHOLD:
            self.frame_counter = 0
            self.frame_processor.process_frame(frame)

        received_points = self.frame_processor.get_frame()
        if received_points is not None:
            print("assign point")
            self.points = received_points

        self.paint_points_on_frame(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
