#!/bin/bash

set -e

echo "📦 Installing dependencies..."
sudo apt update
sudo apt install -y python3-pip libatlas-base-dev libjpeg-dev libtiff-dev libopenjp2-7 libavcodec-dev libavformat-dev libswscale-dev libv4l-dev v4l-utils libgtk-3-dev

pip3 install --upgrade pip
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip3 install opencv-python requests numpy

# Clone YOLOv5
if [ ! -d "yolov5" ]; then
  git clone https://github.com/ultralytics/yolov5.git
  cd yolov5
  pip3 install -r requirements.txt
else
  echo "📁 yolov5 already exists, skipping clone."
fi

# Make detections folder
mkdir -p /home/joetanse/detections

# Reminder for manual camera check
echo "📷 Reminder: Test your Arducam with 'libcamera-still -o test.jpg'"

# Reminder to add cron entry
echo "📝 Reminder: Add the cron @reboot entry manually to crontab."

echo "✅ Setup complete!"
