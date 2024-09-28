import cv2
import os
import mmpose
from mmpose.apis import MMPoseInferencer

from frame_processor import FrameProcessor

class VideoCamera(object):
    FRAME_THRESHOLD = 50

    def __init__(self):
        os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'
        self.video = cv2.VideoCapture(cv2.CAP_V4L2)
        self.frame_processor = FrameProcessor()
        self.frame_counter = 0

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        frame = cv2.flip(frame, 1)
        self.frame_counter = self.frame_counter + 1
        if self.frame_counter == self.FRAME_THRESHOLD:
            self.frame_counter = 0
            self.frame_processor.process_frame(frame)

        processed_frame = self.frame_processor.get_frame()
        if processed_frame is not None:
            frame = processed_frame

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
