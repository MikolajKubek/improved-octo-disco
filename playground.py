import mmpose
from mmpose.apis import MMPoseInferencer

print(mmpose.__version__)

img_path = "poses/test3.jpg"

inferencer = MMPoseInferencer('human')

result_generator = inferencer(img_path, show=True, thickness=5)
result = next(result_generator)
