from flask import Flask, Response
from flask.templating import render_template
from camera import VideoCamera

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def gen(camera):
    camera = VideoCamera()

    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
     return Response(gen(None),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route("/kill_camera")
# def kill_camera():
#    video_stream.__del__()
#    return "Camera destroyed"

@app.route("/hello/<name>")
def hello_there(name=None):
    return render_template("greeting.html", name=name)

@app.route("/camera")
def camera_feed():
    return render_template("camera.html")
