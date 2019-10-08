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


