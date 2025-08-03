from datetime import datetime

import cv2 as cv
import os
import pickle

import cvzone
import numpy as np
import face_recognition

import firebase_admin
from firebase_admin import storage
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate(r'C:\Users\nakul\OneDrive\Desktop\Ai_project\main\serviceAccKey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://hostelleridentification-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket':"hostelleridentification.appspot.com"
})

bucket = storage.bucket()

cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv.imread(r'C:\Users\nakul\OneDrive\Desktop\Ai_project\resources\background.png')

folderModePath = r'C:\Users\nakul\OneDrive\Desktop\Ai_project\resources\Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv.imread(os.path.join(folderModePath, path)))

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

modeType=0
counter=0
id=-1
imgStudent= []


while True:
    success, img = cap.read()

    imgS = cv.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print("matches", matches)
        # print("faceDis", faceDis)

        matchIndex = np.argmin(faceDis)
        # print("Match Index", matchIndex)

        if matches[matchIndex]:
            print("Known Face Detected")
            print(studentIds[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            id = studentIds[matchIndex]
            if counter == 0:
                counter = 1
                modeType=1

    if counter != 0:

        if counter == 1:
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)

            datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                               "%Y-%m-%d %H:%M:%S")
            secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
            print(secondsElapsed)
            if secondsElapsed > 30:
                ref = db.reference(f'Students/{id}')
                studentInfo['total_attendance'] = int(studentInfo['total_attendance'])
                studentInfo['total_attendance'] += 1
                ref.child('total_attendance').set(studentInfo['total_attendance'])
                ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                modeType = 3
                counter = 0
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]



        if 10 < counter < 20:
            modeType = 2

        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if counter <= 10:
            cv.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
            cv.putText(imgBackground, str(studentInfo['Course']), (1006, 550),
                cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv.putText(imgBackground, str(id), (1006, 493),
                 cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            cv.putText(imgBackground, str(studentInfo['Accomodation']), (910, 625),
                cv.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
            cv.putText(imgBackground, str(studentInfo['Current Year']), (1125, 625),
                 cv.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

            (w, h), _ = cv.getTextSize(studentInfo['Name'], cv.FONT_HERSHEY_COMPLEX, 1, 1)
            offset = (414 - w) // 2
            cv.putText(imgBackground, str(studentInfo['Name']), (808 + offset, 445),
                       cv.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)


        counter+=1

        if counter >= 20:
            counter = 0
            modeType = 0
            studentInfo = []
            imgStudent = []
            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


    #cv.imshow("webcam", img)
    cv.imshow("Hosteller Face Detection", imgBackground)
    cv.waitKey(1)


