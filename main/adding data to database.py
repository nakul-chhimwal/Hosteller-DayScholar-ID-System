import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate(r'C:\Users\nakul\OneDrive\Desktop\Ai_project\main\serviceAccKey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://hostelleridentification-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref=db.reference('Students')

data= {
    "E22CSEU0282":
        {
            "total_attendance": "5",
            "Name": " Nakul Chhimwal",
            "Course": "Computer Science",
            "Course Duration": "2022-2026",
            "Accomodation": "Day Scholar",
            "Current Year": "2nd year",
            "last_attendance_time": "2024-04-23 00:54:34"


        },
    "E22CSEU0290":
        {
            "total_attendance": "5",
            "Name": " Akash",
            "Course": "Computer Science",
            "Course Duration": "2022-2026",
            "Accomodation": "Day Scholar",
            "Current Year": "2nd year",
            "last_attendance_time": "2024-04-23 00:54:34"
    },
    "E22CSEU1469":
        {
            "total_attendance": "5",
            "Name": " Arpit",
            "Course": "Computer Science",
            "Course Duration": "2022-2026",
            "Accomodation": "Hosteler",
            "Current Year": "2nd year",
            "last_attendance_time": "2024-04-23 00:54:34"

    },
    "E22CSEU1684":
        {
            "total_attendance": "5",
            "Name": " Kartik",
            "Course": "Computer Science",
            "Course Duration": "2022-2026",
            "Accomodation": "Hosteler",
            "Current Year": "2nd year",
            "last_attendance_time": "2024-04-23 00:54:34"

    },
}

for key,value in data.items():
    ref.child(key).set(value)