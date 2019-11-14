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
	|- model
	|	|- retain_face
	|	|- single_face_model.py
	|	|- utils.py
	|
    |- server
    |  	|- backend_service.py
    |  	|- file_manager.py
	|	|- handlers.py
	|	|- server.py
	|
    |- static
    |  	|- css
    |  	|- js
    |
    |- templates
	|	|- checkin.html
	|	|- dashboard.html
	|	|- login.html
	|	|- manage.html
	|	|- register.html
	|	|- upload.html
	|
	|- test
	|	|-test.py
	|
```



## How  To Use

### Easy run

open the project fold and execute this command, visit localhost:8848/upload to test the upload function.
```
python run.py
```

