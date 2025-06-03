# Motion Detection and Object Classification with YOLOv5 on Raspberry Pi

This project uses a Raspberry Pi (with Arducam 12MP Autofocus V3 camera) to detect motion and classify objects using YOLOv5. When motion is detected, the script runs YOLOv5 inference, logs detections to InfluxDB, and saves annotated images locally for review.
---
## 🚀 Features
- Motion detection using frame differencing
- Object detection with YOLOv5 (runs on CPU)
- Local image annotation and saving of detections
- Logs detections to InfluxDB (label, confidence, and snapshot path)
- Headless operation with auto-start via `cron`
---
## 🧰 Hardware Requirements
- Raspberry Pi 4/5
- Arducam 12MP V3 Autofocus camera
- Storage for saving images
---
## 📦 Dependencies
- Python 3.11+
- OpenCV
- PyTorch
- YOLOv5
- Requests
- NumPy
---
## 🛠️ Installation
Run the provided install script:
```bash
chmod +x install.sh
./install.sh
```
---
## 🧪 Run Manually
```bash
python3 motion_detect_yolov5.py
```
=Or background it:
```bash
nohup python3 motion_detect_yolov5.py > motion.log 2>&1 &
```
---
## 🔁 Auto-start on Boot
Edit crontab:
```bash
crontab -e
```
Add:
```cron
@reboot nohup python3 /home/joetanse/yolov5/motion_detect_yolov5.py > /home/joetanse/yolov5/motion.log 2>&1 &
```
---
## 📂 Output

- Annotated images saved in `/home/joetanse/detections/`
- InfluxDB logs detections with timestamp, label, confidence, and filename
---
## 📊 Example InfluxDB Entry
```
detections,label=person confidence=0.87,filename="frame_20250601_113501.jpg" 1717269301
```
---
## 🧠 Future Enhancements

- Stream annotated snapshots to remote dashboard
- Use a scheduler to throttle detection frequency
- Alert via Discord webhook on specific object classes
---
## 🤝 License
MIT License
---
## 📸 Demo
![sample detection](docs/sample.jpg)
---
## 👨‍💻 Author

Joe Tansey — 2025
