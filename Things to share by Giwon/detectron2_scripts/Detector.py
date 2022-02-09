from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2 import model_zoo

import detectron2
from detectron2.projects import point_rend

import cv2
import numpy as np
import Outputpath


class Detector:
    def __init__(self, model_type="OD"):
        self.cfg = get_cfg()
        self.model_type = model_type

        # Load model config and pretrained model
        # Detectron2 modelzoo : (https://github.com/facebookresearch/detectron2/blob/main/MODEL_ZOO.md)
        if model_type == "OD":  # object detection
            self.cfg.merge_from_file(model_zoo.get_config_file(
                "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
                "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")
        elif model_type == "IS":  # instance segmentation
            self.cfg.merge_from_file(model_zoo.get_config_file(
                "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
                "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        elif model_type == "KP":  # keypoint detection
            self.cfg.merge_from_file(model_zoo.get_config_file(
                "COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
                "COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")
        elif model_type == "LVIS":  # LVIS Segmentation
            self.cfg.merge_from_file(model_zoo.get_config_file(
                "LVISv0.5-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_1x.yaml"))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
                "LVISv0.5-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_1x.yaml")
        elif model_type == "PS":  # Panoptic Segmentation
            self.cfg.merge_from_file(model_zoo.get_config_file(
                "COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml"))
            self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
                "COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml")

        elif model_type == "PR":  # Point Rend clean results in instance segmentation
            # pointrend at [projects/PointRend](https://github.com/facebookresearch/detectron2/tree/main/projects/PointRend#pretrained-models)
            point_rend.add_pointrend_config(self.cfg)
            self.cfg.merge_from_file(
                "/home/appuser/detectron2_repo/projects/PointRend/configs/InstanceSegmentation/pointrend_rcnn_X_101_32x8d_FPN_3x_coco.yaml")
            self.cfg.MODEL.WEIGHTS = "detectron2://PointRend/InstanceSegmentation/pointrend_rcnn_X_101_32x8d_FPN_3x_coco/28119989/model_final_ba17b9.pkl"

        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  # confidency value
        self.cfg.MODEL.DEVICE = "cuda"  # cpu or cuda
        self.predictor = DefaultPredictor(self.cfg)

    # for Images
    def onImage(self, imagePath):
        image = cv2.imread(imagePath)
        output_path = Outputpath.outPath(imagePath)

        if self.model_type != "PS":
            predictions = self.predictor(image)

            # viz = Visualizer(image[:, :, ::-1], metadata=MetadataCatalog.get(
            #     self.cfg.DATASETS.TRAIN[0]), instance_mode=ColorMode.IMAGE_BW)
            # viz = Visualizer(image[:, :, ::-1], metadata=MetadataCatalog.get(
            #     self.cfg.DATASETS.TRAIN[0]), instance_mode=ColorMode.SEGMENTATION)
            viz = Visualizer(
                image[:, :, ::-1], metadata=MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), instance_mode=ColorMode.IMAGE)

            output = viz.draw_instance_predictions(predictions["instances"].to("cpu"))

        else:
            predictions, segmentInfo = self.predictor(image)["panoptic_seg"]
            viz = Visualizer(image[:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]))

            output = viz.draw_panoptic_seg_predictions(predictions.to("cpu"), segmentInfo)

        cv2.imwrite(output_path, output.get_image()[:, :, ::-1])  # OpenCV reads in BGR order
        print("\n\nImage Processing Successful & Saved at : " + output_path + "\n\n")

    # for Videos
    def onVideo(self, videoPath):
        cap = cv2.VideoCapture(videoPath)

        # Check video integrity
        if (cap.isOpened() == False):
            print("Error opening the file...")
            return

        # Input Video properties
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = cap.get(cv2.CAP_PROP_FPS)
        # Video configuration
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = Outputpath.outPath(videoPath)
        # should match input video resolution and framerate (cv2.__version__ = 4.1.2)
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        (success, image) = cap.read()
        print("\n\nVideo Processing Started...\n\n")
        while success:

            if self.model_type != "PS":
                predictions = self.predictor(image)

                # viz = Visualizer(image[:, :, ::-1], metadata=MetadataCatalog.get(
                #     self.cfg.DATASETS.TRAIN[0]), instance_mode=ColorMode.IMAGE_BW)
                # viz = Visualizer(image[:, :, ::-1], metadata=MetadataCatalog.get(
                #     self.cfg.DATASETS.TRAIN[0]), instance_mode=ColorMode.SEGMENTATION)
                viz = Visualizer(
                    image[:, :, ::-1], metadata=MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), instance_mode=ColorMode.IMAGE)

                output = viz.draw_instance_predictions(predictions["instances"].to("cpu"))

            else:
                predictions, segmentInfo = self.predictor(image)["panoptic_seg"]
                viz = Visualizer(image[:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]))

                output = viz.draw_panoptic_seg_predictions(predictions.to("cpu"), segmentInfo)

            # vidout = cv2.resize(output.get_image()[:, :, ::-1], (854, 480))
            out.write(output.get_image()[:, :, ::-1])

            (success, image) = cap.read()

        cap.release()
        print("\n\nVideo Processing Successful & Saved at : " + output_path + "\n\n")
