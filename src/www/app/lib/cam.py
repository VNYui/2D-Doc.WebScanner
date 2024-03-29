import cv2
import sys
import imutils
import numpy as np
#DECODE LIB 
import sys
import zlib
import PIL.Image
import pyzbar.pyzbar
import base45
import cbor2
import pprint

class Cam():
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.detector = cv2.QRCodeDetector()
        self.decoded = type('', (), {})()
        #self.name = cv2.namedWindow("QR CODE READER")
    
    def __del__(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def get_result(self):
        result = {
            'header' : cbor2.loads(self.decoded.value[0]),
            'payload' : cbor2.loads(self.decoded.value[2]),
            'signature' : self.decoded.value[3]
        }
        return result

    def decode(self, img):
            data = pyzbar.pyzbar.decode(img)
            cert = data[0].data.decode()
            b45data = cert.replace("HC1:", "")
            zlibdata = base45.b45decode(b45data)
            cbordata = zlib.decompress(zlibdata)
            self.decoded = cbor2.loads(cbordata)
            print("Header\n----------------")
            pprint.pprint(cbor2.loads(self.decoded.value[0]))
            print("\nPayload\n----------------")
            pprint.pprint(cbor2.loads(self.decoded.value[2]))
            print("\nSignature ?\n----------------")
            print(self.decoded.value[3])
            return self.decoded
    def get_framesAndDecode(self):    
        ret,img = self.cam.read()
        
        # detect and decode
        data, bbox, ret = self.detector.detectAndDecode(img)             
        # decypher B45 and CBOR payload
        if data:
            self.decode(img)
        ret, img = cv2.imencode('.jpg', img)
        return img.tobytes()
