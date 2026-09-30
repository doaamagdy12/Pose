import pyopenpose as op


params = {
    "model_folder": r"D:\Openpose\openpose\models"
}

opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()


def process_frame(frame):

    datum = op.Datum()
    datum.cvInputData = frame

    opWrapper.emplaceAndPop(op.VectorDatum([datum]))

    keypoints = datum.poseKeypoints

    return keypoints.tolist() if keypoints is not None else []