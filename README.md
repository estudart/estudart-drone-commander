# DroneCommander (DJI Tello)

Small Python controller for a **DJI Tello** drone using:

- `djitellopy` for flight commands + video stream
- `pygame` for keyboard input
- `opencv-python` (`cv2`) to display the camera feed
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
python -m pip install djitellopy pygame opencv-python pyttsx3
```

## Run

From the repo root:

```bash
python -m src.main
```

## Controls (default)

- `w` / `a` / `s` / `d`: move forward / left / back / right
- `↑` / `↓`: move up / down
- `r` / `l`: rotate right / rotate left
- `0`: stop (land + stop stream)

## Notes

- Always test in a safe open area.
- Video streaming can take a couple seconds to start after takeoff.
