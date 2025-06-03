import numpy as np
from collections import defaultdict
import subprocess
import time
import cv2
import torch
import requests
from datetime import datetime
from pathlib import Path

last_positions = defaultdict(list)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)
model.conf = 0.3  # confidence threshold

# InfluxDB config
influx_url = "http://localhost:8086/api/v2/write?bucket=birdnet&precision=s"
INFLUX_BUCKET = "birdnet"
INFLUX_ORG = "localorg"
INFLUX_TOKEN = "HzqaSJhhHpPfdbYq4PJ7hawzux5u5_DsQGd5ByYQf0Hpd6vGNd6UwsgV09Q_ieu-dUinROiqHadWBrs_7_pyWg=="
headers = {
    "Authorization": f"Token {INFLUX_TOKEN}",
    "Content-Type": "text/plain"
}

# Paths
snap_path = Path("/tmp/snapshot.jpg")
detections_dir = Path("/home/joetanse/detections")
detections_dir.mkdir(exist_ok=True)
prev_frame = None

print("🔁 Starting motion detection loop...")

def is_moving(label, new_box, threshold=20):
    for prev_box in last_positions[label]:
        prev_x, prev_y = prev_box[:2]
        new_x, new_y = new_box[:2]
        dist = np.linalg.norm([new_x - prev_x, new_y - prev_y])
        if dist < threshold:
            return False
    return True

while True:
    # Take a snapshot with libcamera
    subprocess.run([
        "libcamera-still",
        "--autofocus-mode", "continuous",
        "--autofocus-on-capture",
        "-n", "-t", "100", "-o", str(snap_path)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Load snapshot
    frame = cv2.imread(str(snap_path))
    if frame is None:
        print("⚠️ Snapshot failed, skipping...")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if prev_frame is not None:
        delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        motion_score = thresh.sum()

        print(f"📈 motion_score = {motion_score}")

        if motion_score > 500000000:  # Adjust sensitivity as needed
            print(f"Motion score: {motion_score}")
            print("🚨 Motion detected!")
            results = model(frame)
            results.print()

            # Save rendered frame with YOLO boxes
            results.render()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = detections_dir / f"{timestamp}.jpg"
            cv2.imwrite(str(output_path), results.ims[0])

            # Log filename to InfluxDB
            ts = int(time.time())
            meta_line = f'detections_meta,type="boxed_image" filename="{output_path.name}" {ts}'
            requests.post(influx_url, data=meta_line, headers=headers)

            for *box, conf, cls in results.xyxy[0]:
                label = model.names[int(cls)]
                new_box = box[:2]
                if is_moving(label, new_box):
                    last_positions[label].append(new_box)
                    line = f'detections,label={label} confidence={conf.item():.2f},filename="{output_path.name}" {ts}'
                    requests.post(influx_url, data=line, headers=headers)

    prev_frame = gray
    time.sleep(1)

