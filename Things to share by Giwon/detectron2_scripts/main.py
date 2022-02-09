from Detector import *

# Set detector model type
''' model_type=...
"OD" : Object Detection
"IS" : Instance Segmentation
"KP" : KeyPoint detection
"LVIS" : LVIS segmentation (rate object dataset)
"PS" : Panoptic Segmentation
"PR" : Point Rend (better instance segmentation)
'''
detector = Detector(model_type="PR")

# Image
# detector.onImage("input/image_input1.jpg")

# Video
detector.onVideo("input/video_input1.mp4")
