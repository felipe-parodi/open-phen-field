# Author: Felipe Parodi
# Date: 2023-03-25
# Project: open-phen
# Description: This script takes a video and a detection model and
# outputs a COCO json file with the pose estimation of the detected objects.

import argparse
import json
import os

import cv2
import mmcv
import numpy as np
import matplotlib.pyplot as plt
from mmdet.apis import inference_detector, init_detector

from mmpose.apis import (
    inference_top_down_pose_model,
    init_pose_model,
    process_mmdet_results,
    vis_pose_result,
)
from mmpose.core.post_processing.smoother import Smoother

def main():
    # arguments for the function
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--input-dir", type=str, help="path to the videos")
    parser.add_argument("--output-dir", type=str, help="path to the output directory")
    parser.add_argument(
        "--count", type=int, default=2, help="max number of objects in image"
    )
    parser.add_argument("--device", default="cuda:0", type=str, help="device to use")
    args = parser.parse_args()

    # Load all videos in input directory:
    vid_dir = args.input_dir
    out_dir = args.output_dir
    count = args.count
    device = "cuda:0"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    os.makedirs(out_dir + "/viz", exist_ok=True)
    os.makedirs(out_dir + "/imgs", exist_ok=True)
    os.makedirs(out_dir + "/annotations", exist_ok=True)
    # Set file for output COCO json:
    # use directory name as base for output json file in annotations folder:
    out_json_file = os.path.join(out_dir, "annotations", "keypoints_pseudo.json")
    print(out_json_file)

    # Find and load detection and pose model:
    det_config = "/mmpose/fparodi/open-phen/scripts/faster_rcnn_r50_fpn_conf.py"
    det_checkpoint = "/mmpose/fparodi/open-phen/results/chkpts/sideviewv1/latest.pth"

    # pose model:
    # pose_config = '/mmpose/fparodi/open-phen/scripts/videopose3d_h36m_81frames_fullconv_supervised.py'
    # pose_checkpoint = "https://download.openmmlab.com/mmpose/body3d/videopose/videopose_h36m_81frames_fullconv_supervised-1f2d1104_20210527.pth"
    pose_config = "/mmpose/configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/hrnet_w48_coco_256x192.py"
    pose_checkpoint = "https://download.openmmlab.com/mmpose/top_down/hrnet/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth"

    det_model = init_detector(det_config, det_checkpoint, device=device)
    pose_model = init_pose_model(pose_config, pose_checkpoint, device=device)

    # Load keypoint smoothing configs:
    # g_config = "/mmpose/fparodi/macquad/scripts/pose-estimation/gaussian.py"
    # sg_config = "/mmpose/fparodi/macquad/scripts/pose-estimation/savitzky_golay.py"
    oe_config = "/mmpose/fparodi/macquad/scripts/pose-estimation/one_euro.py"

    # g_smoother = Smoother(filter_cfg=g_config, keypoint_key="keypoints", keypoint_dim=2)
    # sg_smoother = Smoother(
    #     filter_cfg=sg_config, keypoint_key="keypoints", keypoint_dim=2
    # )
    oe_smoother = Smoother(
        filter_cfg=oe_config, keypoint_key="keypoints", keypoint_dim=2
    )

    # Initialize dict for COC file:
    info = {
        "year": "2022",
        "version": "5",
        "description": "Exported from roboflow.ai",
        "contributor": "",
        "url": "https://public.roboflow.ai/object-detection/undefined",
        "date_created": "2022-12-13T11:11:23+00:00",
    }
    licenses = [
        {
            "id": 1,
            "url": "https://creativecommons.org/licenses/by/4.0/",
            "name": "CC BY 4.0",
        }
    ]
    categories = [
        {
            "id": 1,
            "name": "person",
            "supercategory": "person",
            "keypoints": [ # h36m keypoints
                "root", # 0
                "right_hip", # 1
                "right_knee", # 2
                "right_foot", # 3
                "left_hip", # 4
                "left_knee", # 5
                "left_foot", # 6
                "spine", # 7
                "thorax", # 8
                "neck_base", # 9
                "head", # 10
                "left_shoulder", # 11
                "left_elbow", # 12
                "left_wrist", # 13
                "right_shoulder", # 14
                "right_elbow", # 15
                "right_wrist" # 16
            ],
            "skeleton": [
        [0, 1],
        [1, 2],
        [2, 3],
        [0, 4],
        [4, 5],
        [5, 6],
        [0, 7],
        [7, 8],
        [8, 9],
        [9, 10],
        [8, 11],
        [11, 12],
        [12, 13],
        [8, 14],
        [14, 15],
        [15, 16]
            ],
        }
    ]
    img_anno_dict = {
        "info": info,
        "licenses": licenses,
        "categories": categories,
        "images": [],
        "annotations": [],
    }

    kpt_thr = 0.85
    bbox_thr = 0.5
    print('starting loop')
    # loop over all videos in directory
    ann_uniq_id = int(0)
    for vid in os.listdir(vid_dir):
        if not vid.endswith(".avi"):
            continue
        # Load video:
        video = mmcv.VideoReader(vid_dir + vid)
        print(vid)
        # Loop over all frames in video:
        for frame_id, cur_frame in enumerate(mmcv.track_iter_progress(video)):
            # Detect bboxes:
            mmdet_results = inference_detector(det_model, cur_frame)
            bboxes = process_mmdet_results(mmdet_results, cat_id=1)
            if len(bboxes) > count:
                continue
                # bboxes = bboxes[:count]
            # print(bboxes)
            try:
                pose_results, _ = inference_top_down_pose_model(
                    pose_model,
                    cur_frame,
                    bboxes,
                    bbox_thr=bbox_thr, 
                    format="xyxy",
                    dataset=pose_model.cfg.data.test.type,
                    return_heatmap=False,
                    outputs=None,
                    )
            except:
                # print(pose_results)
                continue
            # Smooth keypoints:
            # pose_results = sg_smoother.smooth(pose_results)
            pose_results = oe_smoother.smooth(pose_results)

            # if average confidence score is below threshold, continue to next
            # frame
            if len(pose_results) == 0:
                continue
            if (
                np.mean(
                    [
                        pose_results[0]["keypoints"][j][-1]
                        for j in range(len(pose_results[0]["keypoints"]))
                    ]
                )
                < kpt_thr
            ):
                continue
            annotations_added = False
            # print('Generating COCO annotations for frame', frame_id, '...')
            for indx, i in enumerate(pose_results):
                pose_results[indx]["keypoints"][
                    pose_results[indx]["keypoints"][:, 2] < kpt_thr, :3
                ] = 0
                pose_results[indx]["keypoints"][
                    pose_results[indx]["keypoints"][:, 2] >= kpt_thr, 2
                ] = 2
                x = int(pose_results[indx]["bbox"][0])
                y = int(pose_results[indx]["bbox"][1])
                w = int(pose_results[indx]["bbox"][2] - pose_results[indx]["bbox"][0])
                h = int(pose_results[indx]["bbox"][3] - pose_results[indx]["bbox"][1])
                bbox = [x, y, w, h]
                area = round(w * h, 0)
                center = [x + w / 2, y + h / 2]
                scale = [w / 200, h / 200]
                # add random number to frame_id to make unique
                frame_id_uniq = int(frame_id) + np.random.randint(0, 200000)
                images = {
                    # filename is basename of video + frame number
                    "file_name": os.path.basename(vid)[:-4]
                    + "_"
                    + str(frame_id_uniq)
                    + ".jpg",
                    "height": video.height,
                    "width": video.width,
                    "id": frame_id_uniq,
                }
                annotations = {
                    "keypoints": [
                        int(i)
                        for i in pose_results[indx]["keypoints"].reshape(-1).tolist()
                    ],
                    "num_keypoints": len(
                        pose_results[indx]["keypoints"]
                    ),
                    "area": area,
                    "iscrowd": 0,
                    "image_id": frame_id_uniq,
                    "bbox": bbox,
                    "center": center,
                    "scale": scale,
                    "category_id": 1,
                    "id": ann_uniq_id,
                }

                img_anno_dict["annotations"].append(annotations)
                ann_uniq_id += 1
                annotations_added = True
                raw_frame = (
                    out_dir
                    + "/imgs/"
                    + os.path.basename(vid)[:-4]
                    + "_"
                    + str(frame_id_uniq)
                    + ".jpg"
                )
                cv2.imwrite(raw_frame, cur_frame)
                vis_frame = vis_pose_result(
                    pose_model,
                    cur_frame,
                    pose_results,
                    radius=3,
                    thickness=1,
                    kpt_score_thr=kpt_thr,
                    show=False,
                )
                viz_frame = (
                    out_dir
                    + "/viz/"
                    + os.path.basename(vid)[:-4]
                    + "_"
                    + str(frame_id_uniq)
                    + "_vis.jpg"
                )
                cv2.imwrite(viz_frame, vis_frame)

            if annotations_added:
                img_anno_dict["images"].append(images)
    with open(out_json_file, "w") as outfile:
        json.dump(img_anno_dict, outfile, indent=2)

if __name__ == "__main__":
    main()