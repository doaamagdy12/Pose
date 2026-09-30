import cv2

from services.openpose_service import process_frame


def process_video(video_path):

    capture = cv2.VideoCapture(video_path)

    fps = capture.get(cv2.CAP_PROP_FPS)
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0

    frames = []
    frame_number = 0

    while True:

        success, frame = capture.read()

        if not success:
            break

        keypoints = process_frame(frame)

        frames.append({
            "frame": frame_number,
            "keypoints": keypoints
        })

        frame_number += 1

    capture.release()

    return {
        "fps": fps,
        "totalFrames": total_frames,
        "duration": duration,
        "frames": frames
    }