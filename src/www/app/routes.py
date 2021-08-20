from app import app
from flask import Flask
from flask import render_template, Response, jsonify
from flask_classful import FlaskView, route
from app.lib.cam import Cam
import pprint
import json
import pickle

cam = Cam() 

class ResumeQR(FlaskView):
    # https://localhost:5000/index
    
    def get_nested(self,data, *args):
        if args and data:
            element  = args[0]
            if element:
                value = data.get(element)
                return value if len(args) == 1 else get_nested(value, *args[1:])

    def index(self):
        return Response(self.gen(cam),mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @route('/result')
    def result(self):
        json_data = cam.get_result()
        result = json.loads(json_data)
        return jsonify(result)
        #return render_template('result.html', result=result)
    
    @route('/result-test')
    def test(self):
        #LOAD PICKLE  
        with open('pickle.pickle', 'rb') as f:
            result = pickle.load(f)
        return render_template('result.html', result=result)
        
    def gen(self,camera):
        while True:
            frame = cam.get_framesAndDecode()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

ResumeQR.register(app, route_base='/')   