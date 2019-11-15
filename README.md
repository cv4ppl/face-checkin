# face-checkin

### Overview

Computer Vision Assignment in Soochow Univeristy: a face checkin project.

Membership: Jiacheng Zhang, Han Zhang, Yongchang hao, Renjie Wang.

It contains three part: 

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
├── data
│   ├── database
│   └── mat
├── run.py
├── src
│   ├── android
│   │   └── CheckinApp
│   │       ├── app
│   │       │   ├── build
│   │       │   └── src
│   │       ├── build.gradle
│   │       ├── gradle
│   │       │   └── wrapper
│   │       └── settings.gradle
│   ├── model
│   │   ├── retain_face
│   │   │   ├── data
│   │   │   ├── detect.py
│   │   │   ├── layers
│   │   │   ├── models
│   │   │   ├── train.py
│   │   │   ├── utils
│   │   │   ├── weights
│   │   │   └── widerface_evaluate
│   │   ├── single_face_model.py
│   │   └── utils.py
│   ├── server
│   │   ├── backend_service.py
│   │   ├── file_manager.py
│   │   ├── handlers.py
│   │   └── server.py
│   ├── static
│   │   ├── css
│   │   └── js
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



### Android APK Binary files

Baidu Netdisc:  https://pan.baidu.com/s/1fGFh4u0SNu6YSrgaHqHW7Q 提取码: kjn6 

Google Drive: https://drive.google.com/file/d/1H4a8MV_wK4UwpRP2eXdFViztAan3LI4z/view?usp=sharing



### Online Demo

http://116.62.243.30/



