# face-checkin

### Overview

Computer Vision Assignment in Soochow Univeristy: a face checkin project.

Membership: Jiacheng Zhang, Han Zhang, Yongchang hao, Renjie Wang.

It cotains three part: 

1. Face detection (DNN) and recognition (PCA) model
2. Frontend module ( tornado + bootstrap + jquery )
3. Android app migration

### Workflow
```plain
                  |-----------------|
                  v                 |
           |---------------|      |-----------|
raw.img -> | Page Handlers | ---> | FaceModel |
           |---------------|      |-----------|
                  |                 
                  v
          |----------------|
          | BackendService |
          |----------------|
                  |
                  V
               database
```


### File structure

```plain
.
├── LICENSE
├── README.md
├── data
│   ├── database
│   └── mat
│       ├── F.npy
│       ├── avr.npy
│       ├── dif.npy
│       ├── pt.npy
│       └── uid.npy
├── requirements.txt
├── run.py
├── src
│   ├── android
│   │   └── CheckinApp
│   │       ├── CheckinApp.iml
│   │       ├── app
│   │       │   ├── app.iml
│   │       │   ├── build
│   │       │   ├── build.gradle
│   │       │   ├── libs
│   │       │   ├── proguard-rules.pro
│   │       │   └── src
│   │       ├── build.gradle
│   │       ├── gradle
│   │       │   └── wrapper
│   │       ├── gradle.properties
│   │       ├── gradlew
│   │       ├── gradlew.bat
│   │       ├── local.properties
│   │       └── settings.gradle
│   ├── model
│   │   ├── __pycache__
│   │   │   ├── single_face_model.cpython-37.pyc
│   │   │   └── utils.cpython-37.pyc
│   │   ├── retain_face
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-37.pyc
│   │   │   │   └── detect.cpython-37.pyc
│   │   │   ├── data
│   │   │   │   ├── FDDB
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__
│   │   │   │   ├── config.py
│   │   │   │   ├── data_augment.py
│   │   │   │   └── wider_face.py
│   │   │   ├── detect.py
│   │   │   ├── layers
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__
│   │   │   │   ├── functions
│   │   │   │   └── modules
│   │   │   ├── models
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__
│   │   │   │   ├── net.py
│   │   │   │   └── retinaface.py
│   │   │   ├── train.py
│   │   │   ├── utils
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__
│   │   │   │   ├── box_utils.py
│   │   │   │   ├── nms
│   │   │   │   └── timer.py
│   │   │   ├── weights
│   │   │   │   ├── mobilenet0.25_Final.pth
│   │   │   │   └── mobilenetV1X0.25_pretrain.tar
│   │   │   └── widerface_evaluate
│   │   │       ├── README.md
│   │   │       ├── box_overlaps.pyx
│   │   │       ├── evaluation.py
│   │   │       ├── ground_truth
│   │   │       └── setup.py
│   │   ├── single_face_model.py
│   │   └── utils.py
│   ├── server
│   │   ├── __pycache__
│   │   │   ├── backend_service.cpython-37.pyc
│   │   │   ├── base_handler.cpython-37.pyc
│   │   │   ├── file_manager.cpython-37.pyc
│   │   │   ├── handlers.cpython-37.pyc
│   │   │   ├── login_handler.cpython-37.pyc
│   │   │   ├── server.cpython-37.pyc
│   │   │   └── upload_handler.cpython-37.pyc
│   │   ├── backend_service.py
│   │   ├── file_manager.py
│   │   ├── handlers.py
│   │   └── server.py
│   ├── static
│   │   ├── css
│   │   │   ├── bootstrap-grid.css
│   │   │   ├── bootstrap-grid.css.map
│   │   │   ├── bootstrap-grid.min.css
│   │   │   ├── bootstrap-grid.min.css.map
│   │   │   ├── bootstrap-reboot.css
│   │   │   ├── bootstrap-reboot.css.map
│   │   │   ├── bootstrap-reboot.min.css
│   │   │   ├── bootstrap-reboot.min.css.map
│   │   │   ├── bootstrap.css
│   │   │   ├── bootstrap.css.map
│   │   │   ├── bootstrap.min.css
│   │   │   ├── bootstrap.min.css.map
│   │   │   └── style.css
│   │   └── js
│   │       ├── bootstrap.bundle.js
│   │       ├── bootstrap.bundle.js.map
│   │       ├── bootstrap.bundle.min.js
│   │       ├── bootstrap.bundle.min.js.map
│   │       ├── bootstrap.js
│   │       ├── bootstrap.js.map
│   │       ├── bootstrap.min.js
│   │       ├── bootstrap.min.js.map
│   │       ├── buefy.min.js
│   │       ├── index.js
│   │       ├── jquery.min.js
│   │       ├── md5.js
│   │       └── vue.js
│   ├── templates
│   │   ├── checkin.html
│   │   ├── course.html
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── manage.html
│   │   ├── register.html
│   │   └── upload.html
│   └── test
│       └── test.py
└── tmp
```



## How  To Use

### Execute with source code (Linux & MacOS)

> Currently our software is not validated on Windows platform. (Nov 2019)

Execute this command
```bash
git clone https://github.com/cv4ppl/fack-checkin
cd fack-checkin
pip3 install -r requirements.txt
python3 run.py --port=80 --debug=False
```

> Note: we use python3 and ensure that your python3 version >= 3.6



### Android APK Binary files:

Baidu Netdisc:  https://pan.baidu.com/s/1fGFh4u0SNu6YSrgaHqHW7Q 提取码: kjn6 

Google Drive: https://drive.google.com/file/d/1H4a8MV_wK4UwpRP2eXdFViztAan3LI4z/view?usp=sharing



### Online Demo

http://116.62.243.30/



