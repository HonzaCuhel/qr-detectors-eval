import argparse
import cv2
from enum import Enum
import numpy as np
# import zbarlight
from pyzbar.pyzbar import decode


class TextHelper:
    def __init__(self) -> None:
        self.bg_color = (0, 0, 0)
        self.color = (255, 255, 255)
        self.text_type = cv2.FONT_HERSHEY_SIMPLEX
        self.line_type = cv2.LINE_AA
    def putText(self, frame, text, coords):
        cv2.putText(frame, text, coords, self.text_type, 0.8, self.bg_color, 3, self.line_type)
        cv2.putText(frame, text, coords, self.text_type, 0.8, self.color, 1, self.line_type)
    def rectangle(self, frame, p1, p2, color=None):
        cv2.rectangle(frame, p1, p2, self.bg_color, 6)
        cv2.rectangle(frame, p1, p2, self.color if color is None else color, 1)


class Mode(Enum):
    ALL = 0
    OPENCV = 1
    WECHAT = 2
    PYZBAR = 3


def opencv_qr_detection(frame, opencv_detector, c):
    text, bbox, _ = opencv_detector.detectAndDecode(frame)
    if text == '' and bbox is not None:
        bbox = bbox.astype(int)
        c.rectangle(frame, bbox[0][0], bbox[0][2], color=(0, 0, 255))
    elif text != '' and bbox is not None:
        bbox = bbox.astype(int)
        c.rectangle(frame, bbox[0][0], bbox[0][2])
        c.putText(frame, text, (bbox[0][0][0] + 10, bbox[0][0][1] + 40))
        # data = zbarlight.scan_codes(['qrcode'], img)
    else:
        print("OpenCV wasn't able to detect any QR codes!")


def wechat_qr_detection(frame, wechat_detector, c):
    text, bbox = wechat_detector.detectAndDecode(frame)
    if text == () and bbox != ():
        bbox = [bbox[0].astype(int)]
        c.rectangle(frame, bbox[0][0], bbox[0][2], color=(0, 0, 255))
    elif text != () and bbox != ():
        bbox = [bbox[0].astype(int)]
        c.rectangle(frame, bbox[0][0], bbox[0][2])
        c.putText(frame, text[0], (bbox[0][0][0] + 10, bbox[0][0][1] + 40))
    else:
        # print("WeChatQRCode wasn't able to detect any QR codes!")
        pass


def pyzbar_qr_detection(frame, c):
    qr_decoded = decode(frame)
    if len(qr_decoded) > 0:
        # print(qr_decoded[0].data, qr_decoded[0].polygon)
        bbox = [(int(point.x), int(point.y)) for point in qr_decoded[0].polygon]
        if str(qr_decoded[0].data) == '':
            c.rectangle(frame, bbox[0], bbox[2], color=(0, 0, 255))
        else:
            c.rectangle(frame, bbox[0], bbox[2])
            c.putText(frame, str(qr_decoded[0].data), (bbox[0][0] + 5, bbox[0][1] + 20))
    else:
        print("pyzbar wasn't able to detect any QR codes!")


def eval_qr_detectors(source=0, mode=Mode.OPENCV):
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv2.VideoCapture(source)

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    # Standard OpenCV QR Code detector/decoder
    if mode == Mode.OPENCV or mode == Mode.ALL:
        opencv_detector = cv2.QRCodeDetector()
    # WeChat OpenCV QR Code detector&decode
    if mode == Mode.WECHAT or mode == Mode.ALL:
        wechat_detector = cv2.wechat_qrcode_WeChatQRCode(
            "./WeChatQRCode/detect.prototxt", 
            "./WeChatQRCode/detect.caffemodel", 
            "./WeChatQRCode/sr.prototxt", 
            "./WeChatQRCode/sr.caffemodel"
        )

    c = TextHelper()

    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            # Decode
            # ALL
            if mode == Mode.ALL:
                opencv_frame = frame.copy()
                wechat_frame = frame.copy()
                pyzbar_frame = frame.copy()
                # Run detections
                opencv_qr_detection(opencv_frame, opencv_detector, c)
                wechat_qr_detection(wechat_frame, wechat_detector, c)
                pyzbar_qr_detection(pyzbar_frame, c)
                # Display the resulting frames
                opencvname = 'OpenCV QR detector/decoder'
                cv2.namedWindow(opencvname)        # Create a named window
                cv2.moveWindow(opencvname, 0, 10)  # Move it to (40,30)
                cv2.imshow(opencvname, opencv_frame)
                wechatname = 'WeChat QR detector/decoder'
                cv2.namedWindow(wechatname)        # Create a named window
                cv2.moveWindow(wechatname, 500, 10)  # Move it to (40,30)
                cv2.imshow(wechatname, wechat_frame)
                pyzbarname = 'pzybar QR detector/decoder'
                cv2.namedWindow(pyzbarname)        # Create a named window
                cv2.moveWindow(pyzbarname, 1000, 10)  # Move it to (40,30)
                cv2.imshow(pyzbarname, pyzbar_frame)
            # OpenCV
            elif mode == Mode.OPENCV:
                opencv_qr_detection(frame, opencv_detector, c)
                # Display the resulting frame
                cv2.imshow('Frame', frame)
            # WeChat
            elif mode == Mode.WECHAT:
                wechat_qr_detection(frame, wechat_detector, c)
                # Display the resulting frame
                cv2.imshow('Frame', frame)
            # PyZbar
            elif mode == Mode.PYZBAR:
                pyzbar_qr_detection(frame, c)
                # Display the resulting frame
                cv2.imshow('Frame', frame)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        # Break the loop
        else:
            break
    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Evaluating script for QR detecors&decoders')

    # Source
    parser.add_argument('source', help='A source video feed', nargs='?', default='0')
    # OpenCV
    parser.add_argument('--opencv', action='store_true', help='A standard OpenCV QR code detector/decoder')
    # OpenCV
    parser.add_argument('--wechat', action='store_true', help='A standard WeChat QR code detector/decoder')
    # OpenCV
    parser.add_argument('--pyzbar', action='store_true', help='A standard pyzbar QR code detector/decoder')
    
    args = parser.parse_args()

    mode = Mode.ALL
    if args.opencv:
        mode = Mode.OPENCV
    elif args.wechat:
        mode = Mode.WECHAT
    elif args.pyzbar:
        mode = Mode.PYZBAR
    
    # Parse the source
    source = int(args.source) if args.source.isnumeric() else args.source

    # Evaluate
    # eval_qr_detectors(source='qr_code.avi', mode=mode)
    eval_qr_detectors(source=source, mode=mode)