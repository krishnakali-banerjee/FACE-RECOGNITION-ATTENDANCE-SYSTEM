import cv2
import os
import pickle
import numpy as np
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime


cred = credentials.Certificate("C:\\Computer_Vision\\PROJECT_ATTENDANCE\\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://face-attendance-recognition-default-rtdb.firebaseio.com/",
    'storageBucket' : "face-attendance-recognition.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3,640)       # setting width size
cap.set(4,480)       # setting height size

imgBackground = cv2.imread('C:\\Computer_Vision\\PROJECT_ATTENDANCE\\background.png')

#Importing mode images into a list
folderModePath = 'C:\\Computer_Vision\\PROJECT_ATTENDANCE\\mode'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))    
#print(len(imgModeList))


#load encoding files
file = open('Encode.p','rb')
encodeListKnownwithId = pickle.load(file)
file.close()
encodeListKnown,studentId = encodeListKnownwithId
# print(studentId)

modeType = 0
counter = 0
id=-1
imgStudent=[]

while True:
    ret,img = cap.read()
    
    imgs = cv2.resize(img,(0,0),None,0.25,0.25)
    imgs = cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)
    #cv2.imshow("small image",imgs)
    
    faceCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame = face_recognition.face_encodings(imgs,faceCurFrame)       #location of the face is givem and extract the encode
    
    imgBackground[169:169+480,76:76+640]=img
    imgBackground[35:35+650,842:842+386]=imgModeList[modeType]

    if faceCurFrame:
        for encodeFace in encodeCurFrame:
            for faceLoc in faceCurFrame:
                encodeCurFrame = np.array(encodeCurFrame).reshape(1,-1)
                match = face_recognition.compare_faces(encodeListKnown,encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
                # print("matched",match)
                # print("facedis",faceDis)
            
            matchIndex = np.argmin(faceDis)
            #print("Match Index",matchIndex)
            
            
            if match[matchIndex]:
                # print("Known face detected",studentId[matchIndex])
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                bbox = 75+x1,169+y1,x2-x1,y2-y1
                imgBackground = cvzone.cornerRect(imgBackground,bbox)
                id = studentId[matchIndex]
                
                if counter == 0:
                    cvzone.putTextRect(imgBackground,"Loading",(275,400))
                    cv2.imshow("background",imgBackground) 
                    cv2.waitKey(1)
                    counter =1
                    modeType = 1
            else:
                modeType = 4
                counter = 0
                imgBackground[35:35+650,842:842+386]=imgModeList[modeType]
                
        if counter!=0:
            
            if counter == 1:
                #get the data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                #get the image from the storage
                blob = bucket.get_blob(f'C:\\Computer_Vision\\PROJECT_ATTENDANCE\\people_image/{id}.jpg') #blob
                array = np.frombuffer(blob.download_as_string(), np.uint8)  #array of bytes
                imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)  #actual image
                #update data of attendance
                dateTimeObject = datetime.strptime(studentInfo['last_attendance_time'],"%Y-%m-%d %H:%M:%S")
                
                elapsedTime = (datetime.now()-dateTimeObject).total_seconds()
                print(elapsedTime)
                if elapsedTime>86400:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total attendance'] +=1
                    ref.child('total attendance').set(studentInfo['total attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[35:35+650,842:842+386]=imgModeList[modeType]
            
            if modeType!=3:
            
                if 10<counter<20:
                    modeType = 2
                imgBackground[35:35+650,842:842+386]=imgModeList[modeType]
                
                if counter<=10:
                    cv2.putText(imgBackground,str(studentInfo['total attendance']),(865,125),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
                    cv2.putText(imgBackground,str(id),(1010,482 ),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),1)
                    cv2.putText(imgBackground,str(studentInfo['major']),(1020,545),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),1)
                    cv2.putText(imgBackground,str(studentInfo['grade']),(924,615),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.6,(0,0,0),1)
                    cv2.putText(imgBackground,str(studentInfo['year']),(1050,615),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.6,(0,0,0),1)
                    cv2.putText(imgBackground,str(studentInfo['year_of_joining']),(1177,615),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.6,(0,0,0),1)
                        
                    (w,h),_ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_SIMPLEX,1,2)
                    offset = (386-w)//2
                    cv2.putText(imgBackground,str(studentInfo['name']),(871+offset,425),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2) 
                    
                    
                    imgBackground[172:172+216,927:927+216] = imgStudent
                    
                counter+=1
                
                if counter>=20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[35:35+650,842:842+386]=imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
        imgBackground[35:35+650,842:842+386]=imgModeList[modeType] 
    
    #cv2.imshow("face",frame)
    cv2.imshow("background",imgBackground)
    
    if(cv2.waitKey(1)==ord('x')):
        break
    
cap.release()
cv2.destroyAllWindows()
