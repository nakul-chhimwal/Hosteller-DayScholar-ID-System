import cv2 as cv
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import storage
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate(r'C:\Users\nakul\OneDrive\Desktop\Ai_project\main\serviceAccKey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://hostelleridentification-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket':"hostelleridentification.appspot.com"
})


folderPath = r'C:\Users\nakul\OneDrive\Desktop\Ai_project\Images'
PathList = os.listdir(folderPath)
print(PathList)
imgList = []
studentIds= []
for path in PathList:
    imgList.append(cv.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")