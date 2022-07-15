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