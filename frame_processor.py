from concurrent.futures.thread import ThreadPoolExecutor
from cv2.typing import MatLike
from mmengine.dist.dist import Generator
import mmpose
from mmpose.apis import MMPoseInferencer

import concurrent.futures

from mmpose.apis.visualization import visualize

class FrameProcessor():
    def __init__(self, callback) -> None:
        self.inferencer = MMPoseInferencer('human')
        self.workers = ThreadPoolExecutor(max_workers=1)
        self.future_frame = None
        self.future_callback = callback

    def get_predictions(self, pose_detection_generator):
        print("start generator.next")
        output = next(pose_detection_generator)
        print("generator.next finished")

        predictions_key = "predictions"
        if predictions_key in output and len(output[predictions_key]) > 0:
            top_1_prediction = output[predictions_key][0][0]
            return top_1_prediction

        print(f"no {predictions_key} in output or predictions are empty")
        return None

    def mark_keypoints(self, frame, predictions):
        keypoints_key = "keypoints"
        keypoint_scores_key = "keypoint_scores"
        # print(predictions)
        assert(keypoints_key in predictions)
        assert(keypoint_scores_key in predictions)
        print("predictions len:", len(predictions[keypoints_key]))

        head_points = 5
        hand_points = 11
        leg_points = 17

        head_printed = False
        index = 0
        color = (255, 255, 255)

        points = []

        for coordinates, score in zip(predictions[keypoints_key], predictions[keypoint_scores_key]):
            if index < head_points:
                color = (255, 0, 0)
                if head_printed:
                    index = index + 1
                    continue
                else:
                    head_printed = True

            if index >= head_points and index < hand_points:
                color = (0, 255, 0)

            if index >= hand_points:
                color = (0, 0, 255)

            x, y = coordinates
            if (score < 0.2):
                continue

            points.append((int(x), int(y), color))
            index += index + 1

        print("final points", len(points))

        return points


    def frame_processor_worker(self, frame, pose_detection_generator):
        print("get predictions")
        predictions = self.get_predictions(pose_detection_generator)

        if predictions:
            return self.mark_keypoints(frame, predictions)

        return None

    def process_frame(self, frame: MatLike):
        pose_detection_generator = self.inferencer(frame, show=False, return_datasamples=False, visualize=True)

        num_threads = len(self.workers._threads)

        if self.future_frame is None or self.future_frame.done():
            self.future_frame = self.workers.submit(self.frame_processor_worker, frame, pose_detection_generator)

    def get_frame(self):
        print("future ready")
        if self.future_frame is None:
            return None
        if self.future_frame.done():
            print("future done")
            return self.future_frame.result()

        return None
