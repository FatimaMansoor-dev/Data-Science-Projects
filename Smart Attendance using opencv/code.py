import face_recognition 
import os
import numpy as np 
import csv 
from datetime import datetime
import cv2

vid_cap = cv2.VideoCapture(0)

# Load and encode known faces
shad_img = face_recognition.load_image_file("images/shaddy.jpg")
shad_encoding = face_recognition.face_encodings(shad_img)[0]

virat_img = face_recognition.load_image_file("images/virat.png")
virat_encoding = face_recognition.face_encodings(virat_img)[0]

bisma_img = face_recognition.load_image_file("images/bisma.jpg")
bisma_encoding = face_recognition.face_encodings(bisma_img)[0]

imran_img = face_recognition.load_image_file("images/imran.jpg")
imran_encoding = face_recognition.face_encodings(imran_img)[0]

# Populate known_face_encoding list with actual face encodings
known_face_encoding = [
    shad_encoding,
    virat_encoding,
    bisma_encoding,
    imran_encoding
]

known_faces_names = [
    "shadab",
    "virat",
    "bisma",
    "imran"
]

students = known_faces_names.copy()

face_location = []
face_encoding = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date+'.csv', "w+", newline="")
lnwriter = csv.writer(f)

while True:
    _,frame = vid_cap.read()
    small_frame = cv2.resize(frame,(0,0), fx=0.25, fy=0.25)
    # Convert the image from BGR to RGB since dlib uses RGB format
    rgb_small_frame = small_frame[:, :, ::-1]
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for encode in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding, encode)
            name = 'Unknown'
            face_distances = face_recognition.face_distance(known_face_encoding, encode)
            # identify the person on the frame
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]
            face_names.append(name)
            if name in known_faces_names:
                if name in students:
                    students.remove(name) # TAKAY SRF 1 BAARATTENDANCE LAGAY
                    print(students) 
                    current_time = now.strftime("%H-%M-%S")  # Corrected method name
                    lnwriter.writerow([name, current_time])

    cv2.imshow("attendance system", frame) 
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break      

vid_cap.release()
cv2.destroyAllWindows()
f.close()
