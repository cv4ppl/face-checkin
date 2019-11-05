import cv2
import single_face_model

def detect(filename):
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    img = cv2.imread(filename)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)

    detect_face = []
    for (x,y,w,h) in faces:
        img1 = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        detect_face.append(img[y:y+h,x:x+w])
    return detect_face

def get_ids(detect_face):
    ids = []
    for i in detect_face:
        ids.append(get_id_by_image(i))
    return ids