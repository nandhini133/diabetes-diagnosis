from flask import Flask,render_template, request, url_for
import mysql.connector
import json

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
       


def pred(li):
    li=pd.DataFrame(li)
    data=pd.read_csv("C:\\B Drive\\downloads\\diabetes.csv")
    df=pd.DataFrame(data)
    x=df.iloc[:,:-1]
    y=df.iloc[:,8]
    s1=SVC(kernel='linear',random_state=0)
    s1.fit(x.values,y.values)
    result=s1.predict(li)
    return result

 
app = Flask(__name__)
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="4243",
        database="flask"
        )
cursor = mydb.cursor()

@app.route('/')
def form():
    return render_template('home.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
     
    if request.method == 'POST':

        username = request.form.get("username")
        password = request.form.get("password")
        l=(username,password)
        flag=0
        cursor.execute("select * from login ")
        output = cursor.fetchall()
        for i in output:
            if(l==i):
                print(i)
                flag=1
        if(flag==0):
             return ("login invalid")
        else:
            return render_template("quiz.html")
        
        
    return render_template('login.html')
 
@app.route('/quiz', methods = ['POST', 'GET'])
def quiz():
     
    if request.method == 'POST':
        a=[]
        Pregnancies = int(request.form.get("Pregnancies"))
        Glucose = int (request.form.get("Glucose"))
        BloodPressure = int (request.form.get("BloodPressure"))
        SkinThickness =int (request.form.get("SkinThickness"))
        Insulin = int (request.form.get("Insulin"))
        BMI = float ( request.form.get("BMI"))
        DiabetesPedigreeFunction = float (request.form.get("DiabetesPedigreeFunction"))
        Age = int (request.form.get("Age"))
        li=[[Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age]]
        res=pred(li)
        a=res.tolist()
        if(a[0]==1):
            return "\t Result :\n \t \tyou have diabetes"
        elif (a[0]==0):
            return "\t Result :\n \t \tyou do not have diabetes"


    return render_template("quiz.html")

        
app.run(host='localhost', port=5000)