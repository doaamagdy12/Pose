from flask import Flask

from routes.openpose_routes import openpose_bp


app = Flask(__name__)

app.register_blueprint(openpose_bp)


@app.route("/")
def home():
    return "OpenPose Server is running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)