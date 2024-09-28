from concurrent.futures.thread import ThreadPoolExecutor
from cv2.typing import MatLike
from mmengine.dist.dist import Generator
import mmpose
from mmpose.apis import MMPoseInferencer

import concurrent.futures

class FrameProcessor():
    def __init__(self) -> None:
        self.inferencer = MMPoseInferencer('human')
        self.workers = ThreadPoolExecutor(max_workers=1)
        self.future_frame = None

    def frame_processor_worker(self, pose_detection_generator):
        return next(pose_detection_generator)


    def process_frame(self, frame: MatLike):
        pose_detection_generator = self.inferencer(frame, show=False, return_datasamples=True)

        self.future_frame = self.workers.submit(self.frame_processor_worker, pose_detection_generator)

    def get_frame(self):
        if self.future_frame and self.future_frame.done():
            return self.future_frame.result()
        return None
