import torch

# Model
model = torch.hub.load("ultralytics/yolov5", "yolov5s")  # or yolov5n - yolov5x6, custom

# Images
img = "https://ultralytics.com/images/zidane.jpg"  # or file, Path, PIL, OpenCV, numpy, list
# img = "https://www.kgnews.co.kr/data/photos/20211144/art_16358342805544_15e50c.jpg"  # or file, Path, PIL, OpenCV, numpy, list
# img = "https://cdn.lecturernews.com/news/photo/202301/117520_353732_5812.jpg"  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
# results.print()  # or .show(), .save(), .crop(), .pandas(), etc.

# results.show()

# print(results.xyxy[0])
print(results.pandas().xyxy[0])
