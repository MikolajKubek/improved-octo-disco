import cv2
import os
import mmpose
from mmpose.apis import MMPoseInferencer

class VideoCamera(object):
    def __init__(self):
        os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'
        self.video = cv2.VideoCapture(cv2.CAP_V4L2)
        self.inferencer = MMPoseInferencer('human')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        out = self.inferencer(frame, show=False, return_datasamples=True)
        print(next(out))

        # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV
        frame = cv2.flip(frame, 1)

       # self.inferencer(frame, show=False)

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
