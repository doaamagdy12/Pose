def validate_move_name(name):

    if not name or not name.strip():
        return False, "Move name is required"

    if len(name.strip()) < 3:
        return False, "Move name must be at least 3 characters"

    return True, None


def validate_video(video):

    if video is None or video.filename == "":
        return False, "Video is required"

    return True, None