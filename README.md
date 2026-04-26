# DroneCommander (DJI Tello)

Small Python controller for a **DJI Tello** drone using:

- `djitellopy` for flight commands + video stream
- `opencv-python` (`cv2`) to display the camera feed
- `ultralytics` (YOLO) for threat detection
- `pyttsx3` for optional text-to-speech feedback

## What it does

- Starts the Tello connection
- Takes off
- Turns on the video stream and shows it in an OpenCV window
- Reads keyboard input and sends movement/rotation commands via a background worker thread

## Requirements

- A DJI Tello drone
- Your computer connected to the Tello Wi‑Fi network
- Python 3.x

Install dependencies (example):

```bash
python -m pip install djitellopy opencv-python pyttsx3 ultralytics
```

## Knife model (recommended)

The default threat detector is configured for a **weapon-specific YOLOv8n model** (knife/gun/grenade/explosion) that expects **imgsz=960**.

- Download the checkpoint and place it here:
  - `weights/weapon-detection-yolov8n-v2-best.pt`
- Source: SyncRobotic “Weapon Detection YOLOv8n v2” on Hugging Face.

## Run

From the repo root:

```bash
python -m src.main
```

## Controls (default)

- `w` / `a` / `s` / `d`: move forward / left / back / right
- `i` / `k` (or `+` / `-`): move up / down
- `r` / `l` (or `e` / `q`): rotate right / rotate left
- `0`: stop (land + stop stream)

## Notes

- Always test in a safe open area.
- Video streaming can take a couple seconds to start after takeoff.
