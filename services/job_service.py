import json
import os
import uuid


def create_job_id():
    return f"move_{uuid.uuid4().hex[:8]}"


def save_result(job_id, result):

    os.makedirs("outputs", exist_ok=True)

    output_path = f"outputs/{job_id}.json"

    data = {
        "jobId": job_id,
        "name": result["name"],
        "fps": result["fps"],
        "totalFrames": result["totalFrames"],
        "duration": result["duration"],
        "frames": result["frames"]
    }

    with open(output_path, "w") as file:
        json.dump(data, file, indent=2)

    return output_path

def get_result(job_id):

    output_path = f"outputs/{job_id}.json"

    if not os.path.exists(output_path):
        return None

    with open(output_path, "r") as file:
        result = json.load(file)

    return {
        "jobId": result["jobId"],
        "name": result["name"],
        "fps": result["fps"],
        "totalFrames": result["totalFrames"],
        "duration": result["duration"],
        "frames": result["frames"]
    }

def update_move_name(job_id, name):

    output_path = f"outputs/{job_id}.json"

    if not os.path.exists(output_path):
        return None

    with open(output_path, "r") as file:
        result = json.load(file)

    result["name"] = name

    with open(output_path, "w") as file:
        json.dump(result, file, indent=2)

    return result