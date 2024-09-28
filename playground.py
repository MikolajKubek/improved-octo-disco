import mmpose
from mmpose.apis import MMPoseInferencer

print(mmpose.__version__)

img_path = "poses/downward_facing_dog.jpg"

inferencer = MMPoseInferencer('human')

result_generator = inferencer(img_path, show=True)
# result = next(result_generator)

# print(result)
