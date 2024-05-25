import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("C:\\Computer_Vision\\PROJECT_ATTENDANCE\\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://face-attendance-recognition-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data ={                                      #dictionary
    "1001":{                                 #keys
        "name": "Krishnakali Banerjee",        #values
        "major": "CSE",
        "year": "2nd",
        "total attendance": 5,
        "year_of_joining":2021,
        "grade":8.9,
        "last_attendance_time":"2023-06-02 07:15:35"
    },
    # "1002":{                                 #keys
    #     "name": "Kriti Srivastave",        #values
    #     "major": "CSE",
    #     "year": "3rd",
    #     "total attendance": 8,
    #     "year_of_joining":2021,
    #     "grade":7.5,
    #     "last_attendance_time":"2023-06-02 07:15:35"
    # },
    # "1003":{                                 #keys
    #     "name": "Madhusnuhi Panda",        #values
    #     "major": "CSE",
    #     "year": "3rd",
    #     "total attendance": 10,
    #     "year_of_joining":2021,
    #     "grade":9.5,
    #     "last_attendance_time":"2023-06-02 07:15:35"
    # },
    # "1004":{                                 #keys
    #     "name": "Nitu Kumari",        #values
    #     "major": "CSE",
    #     "year": "3rd",
    #     "total attendance": 4,
    #     "year_of_joining":2021,
    #     "grade":8.1,
    #     "last_attendance_time":"2023-06-01 05:56:00"
    # },
    "1005":{                                 #keys
        "name": "Sayan Banerjee",        #values
        "major": "CSE",
        "year": "3rd",
        "total attendance": 6,
        "year_of_joining":2021,
        "grade":9.0,
        "last_attendance_time":"2023-06-03 07:38:00"
    },
    "1006":{                                 #keys
        "name": "Supriti Paria",        #values
        "major": "CSE",
        "year": "3rd",
        "total attendance": 5,
        "year_of_joining":2021,
        "grade":9.1,
        "last_attendance_time":"2023-06-01 05:56:00"
    },
    "1007":{                                 #keys
        "name": "Biswajit Banerjee",        #values
        "major": "MECH",
        "year": "4th",
        "total attendance": 0,
        "year_of_joining":2020,
        "grade":9.1,
        "last_attendance_time":"2023-06-02 06:00:00"
    },
    "1008":{                                 #keys
        "name": "Anwesha Das",        #values
        "major": "CSE",
        "year": "1st",
        "total attendance": 10,
        "year_of_joining":2023,
        "grade":9.4,
        "last_attendance_time":"2023-06-05 06:09:00"
    },
    "1009":{                                 #keys
        "name": "Sutapa Dasgupta",        #values
        "major": "ECE",
        "year": "4th",
        "total attendance": 8,
        "year_of_joining":2020,
        "grade":9.1,
        "last_attendance_time":"2023-06-02 03:00:11"
    },
    "2005":{                                 #keys
        "name": "Harry Styles",        #values
        "major": "ECE",
        "year": "3rd",
        "total attendance": 8,
        "year_of_joining":2020,
        "grade":7.5,
        "last_attendance_time":"2023-06-01 05:56:00"
    },
    "5008":{                                 #keys
        "name": "Kim Seokjin",        #values
        "major": "CSSE",
        "year": "1st",
        "total attendance": 3,
        "year_of_joining":2022,
        "grade":9.2,
        "last_attendance_time":"2023-06-02 08:30:23"
    },
    "6009":{                                 #keys
        "name": "Arindam Dasgupta",        #values
        "major": "CSE",
        "year": "4th",
        "total attendance": 8,
        "year_of_joining":2022,
        "grade":9.2,
        "last_attendance_time":"2023-06-05 08:30:33"
    },
    "5007":{
        "name":"Gautam Paul",
        "major":"CSE",
        "year":"4th",
        "total attendance": 0,
        "year_of_joining":2022,
        "grade":9.2,
        "last_attendance_time":"2023-06-04 08:31:33"
    },
    # "3002":{
    #     "name":"Sonali Banerjee",
    #     "major":"CSE",
    #     "year":"3rd",
    #     "total attendance": 2,
    #     "year_of_joining":2022,
    #     "grade":9.2,
    #     "last_attendance_time":"2023-02-04 08:31:33"
    # }
    
    
}

for key,values in data.items():
    ref.child(key).set(values)