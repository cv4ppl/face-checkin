# face-checkin

### Overview

### Workflow
```plain
                  |-----------------|
                  v                 |
           |---------------|      |-----------|
raw.img -> | UploadHandler | ---> | FaceModel |
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
- /
  |- src
     |- server
     |  |- upload_handler.py
     |  |- backend_service.py
     |
     |- model
     |  |- img2id.py
     |
     |- templates
        |- upload.html
        |- dashboard.html
```



## How  To Use

### Easy run

open the project fold and execute this command, visit localhost:8848/upload to test the upload function.
```
python run.py
```

