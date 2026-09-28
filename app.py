from flask import Flask, request, jsonify
import cv2
import numpy as np
import pyopenpose as op

app = Flask(__name__)

params = {
    "model_folder": r"D:\Openpose\openpose\models"
}

opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()


@app.route("/")
def home():
    return "OpenPose Server is running!"


@app.route("/openpose/video", methods=["POST"])
def process_video():
    video = request.files["video"]

    video_path = "temp_video.mp4"
    video.save(video_path)

    capture = cv2.VideoCapture(video_path)

    frames = []
    frame_number = 0

    while True:
        success, frame = capture.read()

        if not success:
            break

        datum = op.Datum()
        datum.cvInputData = frame

        opWrapper.emplaceAndPop(op.VectorDatum([datum]))

        keypoints = datum.poseKeypoints

        frames.append({
            "frame": frame_number,
            "keypoints": keypoints.tolist() if keypoints is not None else []
        })

        frame_number += 1

    capture.release()

    job_id = "move_001"

    output_path = f"outputs/{job_id}.json"

    with open(output_path, "w") as file:
        import json
        json.dump({
            "jobId": job_id,
            "frames": frames
        }, file)

    return jsonify({
        "success": True,
        "jobId": job_id
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)