#!/usr/bin/env python3
import os
from pathlib import Path

import cv2


dataset = Path(os.environ.get("MCGS_GARDEN", "/datasets/garden"))
cameras = (
    "front_left",
    "front_center",
    "front_right",
    "left_center",
    "right_center",
)

if not dataset.is_dir():
    raise SystemExit(f"Garden dataset is not mounted at {dataset}")

reference_names = None
for camera in cameras:
    image_dir = dataset / "images" / camera
    names = sorted(path.name for path in image_dir.glob("*.png"))
    if len(names) != 217:
        raise SystemExit(f"Expected 217 PNG files in {image_dir}, found {len(names)}")
    if reference_names is None:
        reference_names = names
    elif names != reference_names:
        raise SystemExit(f"Camera timestamps are not synchronized in {image_dir}")

    image = cv2.imread(str(image_dir / names[0]))
    if image is None or image.shape[:2] != (480, 640):
        shape = None if image is None else image.shape[:2]
        raise SystemExit(f"Expected 640x480 images in {image_dir}, found {shape}")

if os.access(dataset, os.W_OK):
    raise SystemExit(f"Dataset mount must be read-only: {dataset}")

print(f"Garden dataset: OK ({len(cameras)} cameras, 217 synchronized 640x480 frames)")
