import math
CONFIDENCE_THRESHOLD = 0.5

def get_direction(angle):
    if -22.5 <= angle < 22.5:
        return "right"

    if 22.5 <= angle < 67.5:
        return "down-right"

    if 67.5 <= angle < 112.5:
        return "down"

    if 112.5 <= angle < 157.5:
        return "down-left"

    if angle >= 157.5 or angle < -157.5:
        return "left"

    if -157.5 <= angle < -112.5:
        return "up-left"

    if -112.5 <= angle < -67.5:
        return "up"

    return "up-right"

def calculate_movement(point1, point2, fps):
    # Get x, y coordinates and confidence for both points
    x1, y1, confidence1 = point1
    x2, y2, confidence2 = point2

    # Skip the movement calculation if either point has low confidence
    if confidence1 < CONFIDENCE_THRESHOLD or confidence2 < CONFIDENCE_THRESHOLD:
        return None


    # Calculate movement on x and y axes
    dx = x2 - x1
    dy = y2 - y1

    # Calculate the total distance traveled
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # Calculate time between two frames
    time = 1 / fps

    # Calculate speed
    speed = distance / time

    # Calculate movement angle
    angle = math.degrees(math.atan2(dy, dx))
    direction = get_direction(angle)

    return {
        "dx": dx,
        "dy": dy,
        "distance": distance,
        "speed": speed,
        "angle": angle,
        "direction": direction,
        "confidence": min(confidence1, confidence2)
    }


def analyze_keypoint(frames, keypoint_index, fps):
    movements = []

    # Compare each frame with the next frame
    for i in range(len(frames) - 1):
        point1 = frames[i]["keypoints"][0][keypoint_index]
        point2 = frames[i + 1]["keypoints"][0][keypoint_index]

        # Calculate movement between the two points
        movement = calculate_movement(point1, point2, fps)

        # Skip frames with low-confidence keypoints
        if movement is None:
            continue
        
        movements.append({
            "fromFrame": frames[i]["frame"],
            "toFrame": frames[i + 1]["frame"],
            **movement
        })

    return movements