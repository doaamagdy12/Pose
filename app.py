from flask import Flask, request, jsonify
import cv2
import pyopenpose as op
import os
import json
import uuid  # to generate unique job IDs

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

# Post endpoint to process video and extract pose keypoints
@app.route("/openpose/video", methods=["POST"])
def process_video():

    video = request.files["video"]

    video_path = "temp_video.mp4"
    video.save(video_path)

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

    job_id = f"move_{uuid.uuid4().hex[:8]}"

    os.makedirs("outputs", exist_ok=True)

    output_path = f"outputs/{job_id}.json"

    with open(output_path, "w") as file:
        json.dump({
            "jobId": job_id,
            "fps": fps,
            "totalFrames": total_frames,
            "duration": duration,
            "frames": frames
        }, file, indent=2)

    return jsonify({
        "success": True,
        "jobId": job_id
    })

# Get endpoint to retrieve the result of a specific job
@app.route("/openpose/result/<job_id>", methods=["GET"])
def get_result(job_id):
    output_path = f"outputs/{job_id}.json"
    if not os.path.exists(output_path):
        return jsonify({
            "success": False,
            "message": "Job not found"
        }), 404

    with open(output_path, "r") as file:
        result = json.load(file)

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)