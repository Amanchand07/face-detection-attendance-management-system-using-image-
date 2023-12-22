from ntpath import join

from pyttsx3 import speak
from student_detail import Student
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import re
import os
import numpy as np
from time import strftime
from datetime import datetime
import cv2 as cv
# import pyttsx3
from os.path import isfile,join
from os import listdir
import time
import pandas as pd
import csv
import pyttsx3


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 is for female voice and 0 is for male voice


def speak_va(transcribed_query):
    engine.say(transcribed_query)
    engine.runAndWait()


class Face_Recognition:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")


        title_lbl=Label(self.root,text="FACE RECOGNITION",font=("Algerian",20,"bold"),bg="lightblue",fg="darkgreen")
        title_lbl.place(x=0,y=0,width=1366,height=35)

       #first image
        # img_top=Image.open(r"Images\n.jpg")
        # img_top=img_top.resize((630, 650),Image.LANCZOS)
        # self.photoimg_top=ImageTk.PhotoImage(img_top)

        # f_lbl=Label(self.root,image=self.photoimg_top)
        # f_lbl.place(x=0,y=45,width=630,height=650)
        
        # second image
        img_bottom=Image.open(r"C:\Users\amanc\OneDrive\Desktop\Attendance-Management-System-using-OpenCV-main\Attendance-Management-System-using-OpenCV-main\Images\re1.jpg")
        # img_bottom = Image.open(r"C:\Users\ACER\Desktop\myProj\Facial-Recognition-Based-Student-Attendance-System\Images\re1.jpg")
        img_bottom = img_bottom.resize((1366, 700),Image.LANCZOS)
        self.photoimg_bottom=ImageTk.PhotoImage(img_bottom)

        f_lbl=Label(self.root,image=self.photoimg_bottom)
        f_lbl.place(x=0,y=50,width=1366,height=650)
        
        # Button
        b1_1=Button(f_lbl,text="Face Recognition",cursor="hand2",command=self.face_recog,font=("Algerian",15,"bold"),bg="darkgreen",fg="yellow")
        b1_1.place(x=500,y=450,width=300,height=150)






    


        # =================Attendance ====================
    # def mark_attendance(self,i,r,n,d):
    def mark_attendance(self,i,r,n,d):
        with open(r"C:\Users\amanc\OneDrive\Desktop\Attendance-Management-System-using-OpenCV-main\Attendance-Management-System-using-OpenCV-main\Shivansh.csv","r+",newline="\n") as f:
            
            # f.drop_duplicates()
            myDatalist=f.readlines()
            name_list=[]
            for line in myDatalist:
                entry=line.split(" ")
                name_list.append(entry[0])
            if((i not in name_list) and (r not in name_list) and (n not in name_list) and (i not in name_list)):
                now=datetime.now()
                d1=now.strftime("%d/%m/%Y")
                # d1 for date variable
                dtString=now.strftime("%H:%M:%S")
                # myDatalist.drop_duplicates(keep=False)
             

                f.writelines(f"\n{i},{r},{n},{d},{dtString}, {d1},Present{i}")



     # face recognition  command=self.face_recog
    def face_recog(self):
        def draw_boundray(img,classifier,scaleFactor,minNeighbors,color,text,clf):
            gray_image= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features= classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)   

            coord=[]
            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w+20,y+h+20),(0,255,0),3)
                id,predict=clf.predict(gray_image[y:y+h+20,x:x+w+20])
                # confidence=int((100*(1-predict/300)))

                conn = mysql.connector.connect(host="localhost", user="root", password="root", database="face_recognition")
                # conn=mysql.connector.connect(host="localhost",username="root",password="Keshav@123",database="mydata")
                my_cursor=conn.cursor()

                my_cursor.execute("select Name from student1 where id="+str(id))
                n = my_cursor.fetchone()

                n = str(n)
                print(n)
                # n="+".join(n)

                my_cursor.execute("select Roll from student1 where id="+str(id))
                r=my_cursor.fetchone()
                r = str(r)
                # r = "+".join(r)

                
                my_cursor.execute("select Dep from student1 where id="+str(id))
                d=my_cursor.fetchone()
                d = str(d)
                # d = "+".join(d)

                my_cursor.execute("select id from student1 where id="+str(id))
                i=my_cursor.fetchone()
                i = str(i)
                # i = "+".join(i)
                
                # new code for accuracy calculation
                # img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                # result = id.predict(img)

                if predict < 500:
                # if result[1] < 500:
                    confidence=int((100*(1-predict/300)))
                    # str2 = str(confidence)
                    # confidence = int(100 * (1 - (result[1])/300))
                    # display_string = str(confidence)+'% confidence it is user'
                # cv2.putText(img,display_string(250, 250), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
                    cv2.putText(img,f"Accuracy:{confidence}%",(x, y-100), cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),3)



                if confidence> 70:
                    cv2.putText(img,f"id: {i}",(x,y-75),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Roll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Name:{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Department:{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    self.mark_attendance(i,r,n,d)

                else:
                    cv2.rectangle(img,(x,y),(x+w+20,y+h+20),(0,0,255),3)
                    speak_va("Warning!!! Unknown Face")
                    cv2.putText(img,"Unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)

                coord=[x,y,w,h]

            return coord 
            
        def recognize(img,clf,faceCascade):
            coord = draw_boundray(img, faceCascade, 1.1, 10, (255,25,255), "Face", clf)   
            return img
        
        faceCascade=cv2.CascadeClassifier(r"C:\Users\amanc\OneDrive\Desktop\Attendance-Management-System-using-OpenCV-main\Attendance-Management-System-using-OpenCV-main\haarcascade_frontalface_default.xml")
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.read(r"C:\Users\amanc\OneDrive\Desktop\Attendance-Management-System-using-OpenCV-main\Attendance-Management-System-using-OpenCV-main\classifier.xml")

        video_cap=cv2.VideoCapture(0)
        
        while True:
            ret,img=video_cap.read()
            img=recognize(img,clf,faceCascade)
            # speak_va("Welcome to Face Recognition World")
            cv2.imshow("Welcome to face Recognition",img)


            if cv2.waitKey(1)==13:
                
                break
        video_cap.release()
        cv2.destroyAllWindows()

        df_state = pd.read_csv(r"C:\Users\amanc\OneDrive\Desktop\Attendance-Management-System-using-OpenCV-main\Attendance-Management-System-using-OpenCV-main\Shivansh.csv")
    

        DF_RM_DUP = df_state.drop_duplicates(keep=False) 
        DF_RM_DUP.to_csv(r'C:\Users\amanc\OneDrive\Desktop\Attendance-Management-System-using-OpenCV-main\Attendance-Management-System-using-OpenCV-main\test1.csv', index=False) 


if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition(root)
    root.mainloop()
