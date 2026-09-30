from flask import Blueprint, request, jsonify

from services.video_service import process_video
from services.job_service import (
    create_job_id,
    save_result,
    get_result,
    update_move_name
)


openpose_bp = Blueprint("openpose", __name__)


@openpose_bp.route("/openpose/video", methods=["POST"])
def process_video_route():

    video = request.files["video"]
    name = request.form.get("name", "Untitled Move")

    video_path = "temp_video.mp4"
    video.save(video_path)

    job_id = create_job_id()

    result = process_video(video_path)

    result["name"] = name

    save_result(job_id, result)

    return jsonify({
        "success": True,
        "jobId": job_id,
        "name": name,
        "fps": result["fps"], 
    })


@openpose_bp.route("/openpose/result/<job_id>", methods=["GET"])
def get_result_route(job_id):

    result = get_result(job_id)

    if result is None:
        return jsonify({
            "success": False,
            "message": "Job not found"
        }), 404

    return jsonify(result)


@openpose_bp.route("/openpose/move/<job_id>", methods=["PUT"])
def update_move(job_id):

    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({
            "success": False,
            "message": "Name is required"
        }), 400

    result = update_move_name(job_id, data["name"])

    if result is None:
        return jsonify({
            "success": False,
            "message": "Job not found"
        }), 404

    return jsonify({
        "success": True,
        "jobId": job_id,
        "name": result["name"]
    })