# QR Code detectors/decoders evaluating script

## Install project requirements

```
# Linux
sudo apt-get install libzbar0
# Mac OS X
sudo apt-get install libzbar0
python3 -m pip install -r requirements.txt
```

## Usage

```
python3 main.py [-h] [--opencv] [--wechat] [--pyzbar] [source]
```

- `-h` for help
- `--opencv` for using standard OpenCV QR code detector/decoder
- `--wechat` for using standard WeChat QR code detector/decoder
- `--opencv` for using standard OpenCV QR code detector/decoder
- `source` for defining source of a video feed (e.g. `0` for web camera)

## Running

```
# Default run with all QR code detectors/decoders and camera video feed
python3 main.py
# Default run with all QR code detectors/decoders and video feed
python3 main.py qr_code.avi
# Help
python3 main.py - h
# Default run with WeChat QR code detector/decoder and camera video feed
python3 main.py --wechat
# Default run with WeChat QR code detector/decoder and video file
python3 main.py --wechat qr_code.avi
```

## Materials

### OpenCV

- https://docs.opencv.org/4.x/de/dc3/classcv_1_1QRCodeDetector.html
- https://learnopencv.com/opencv-qr-code-scanner-c-and-python/ 

### WeChat

- https://docs.opencv.org/4.x/d5/d04/classcv_1_1wechat__qrcode_1_1WeChatQRCode.html
- https://learnopencv.com/wechat-qr-code-scanner-in-opencv/

### pyzbar

- https://pypi.org/project/pyzbar/