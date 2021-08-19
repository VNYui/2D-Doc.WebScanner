from app import app
from flask import Flask
from flask import render_template, Response
from flask_classful import FlaskView, route
from app.lib.cam import Cam
cam = Cam() 

class ResumeQR(FlaskView):
    # https://localhost:5000/index

    def index(self):
        return Response(self.gen(cam),mimetype='multipart/x-mixed-replace; boundary=frame')

    def gen(self,camera):
        while True:
            frame = cam.get_framesAndDecode()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

ResumeQR.register(app, route_base='/')   