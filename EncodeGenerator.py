import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("C:\\Computer_Vision\\PROJECT_ATTENDANCE\\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://face-attendance-recognition-default-rtdb.firebaseio.com/",
    'storageBucket' : "face-attendance-recognition.appspot.com"
})



#Importing people images into a list
folderPath = 'C:\\Computer_Vision\\PROJECT_ATTENDANCE\\people_image'
pathList = os.listdir(folderPath)
#print(pathList)     used for printing the image name
imgList = []
studentId = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentId.append(os.path.splitext(path)[0])
    
    #adding images to the database
    
    fileName = f'{folderPath}/{path}'
    print(fileName)
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    # blob.upload_from_filename(fileName)

#print(path)    id are given as the name of the image
#print(os.path.splitext(path)[0])    used for extracting the id from the name
#print(len(imgList))

def findEncode(imageList):
    encodeList=[]
    for img in imageList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(img)  #0 is for finding the first element of endoings
        if len(face_encodings) > 0:
            encode = face_encodings[0]
            encodeList.append(encode)
        # else:
        #     print(f"No face found in the image: {img}")
    
    return encodeList

encodeListKnown=findEncode(imgList)
encodeListKnownwithId = [encodeListKnown,studentId]
#print(encodeListKnown)

file = open("Encode.p",'wb')
pickle.dump(encodeListKnownwithId,file)
file.close()
print("file saved")