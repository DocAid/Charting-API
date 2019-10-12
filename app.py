
from flask import Flask, redirect, url_for, request, jsonify,render_template
from firebase_admin import credentials, firestore, initialize_app
import pickle
import socket
import json
import requests
import matplotlib.pyplot as plt
import matplotlib
import pyrebase
from skimage import io

from matplotlib.patches import Arrow, Circle
import pdfkit
import sklearn
app = Flask(__name__)
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()

config = {
       "apiKey": "AIzaSyAmAnf-0bRmvGjRkJJgpZkDiZ3nRIFlBhw",
    "authDomain": "docaid-api.firebaseapp.com",
    "databaseURL": "https://docaid-api.firebaseio.com",
    "projectId": "docaid-api",
    "storageBucket": "docaid-api.appspot.com",
    "messagingSenderId": "918014081942",
    "appId": "1:918014081942:web:827def8f7c8615204d7bb7"

}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

patient_details = db.collection('patient_details')
medicines_diagonized = db.collection('medicines_diagonized')
diagnosis_keywords = db.collection('diagnosis_keywords')
reports = db.collection('reportsUrl')
charts1 = db.collection('charts1')
charts2 = db.collection('charts2')




@app.route('/rg',methods=['POST'])
def genPdf():
    if request.method == 'POST':
        data = request.json
        age = data['age']
        pid = data['pid']
        dosages = data['dosages']
        bmi = data['bmi']
        img1 = 'https://firebasestorage.googleapis.com/v0/b/docaid-api.appspot.com/o/img1.jpg?alt=media&token=63ba5fe0-d6a7-42e9-8644-129c85725845'
        img2 = 'https://firebasestorage.googleapis.com/v0/b/docaid-api.appspot.com/o/img2.png?alt=media&token=18f4aa32-badf-4104-9e85-693dd8a96561'
        x = render_template('r.html',pid=pid,age=age,bmi=bmi,dosages=dosages,img1=img1,img2=img2)
        print(type(x))
        print(x)
        pdfkit.from_string(x,'report1.pdf')
        report = str(pid)
        storage.child('reportsPdf/{}'.format(report)).put('report1.pdf')
        pdf_url = storage.child('reportsPdf/{}'.format(report)).get_url(None)
        data = {
            'pdf_url':pdf_url
        }
        res = reports.document(pid).set(data)
        return pdf_url

  
@app.route('/sendReportToDB',methods=['POST'])
def getReport():
    requestData = request.json
    pid = requestData['pid']
    data = reports.document(pid).get()
    return jsonify(data.to_dict())



@app.route('/charts1',methods=['POST'])
def chart1():
    r = request.json
    pid = r['pid']
    print(pid)
    res = requests.get('http://34.93.231.96:5000/keywords',json={'pid':pid})
    data = res.json()
    totalPositiveSymps = []
    i = 0
    a = 0
    for da in data:
        temp = data[da]
        for key in temp.keys():
            temp1 = temp[key]
            temp2 = temp1['symptoms']
            for k in temp2.keys():
                print(type(temp2[k]))
                if temp2[k] == True:
                    a +=1
            break
        i+=1
        if i%2 == 0:
            i = 0
            totalPositiveSymps.append(a)
    for i in range(1,len(totalPositiveSymps)):
        totalPositiveSymps[i] = totalPositiveSymps[i]-totalPositiveSymps[i-1] 
    dateStr = ['1-3','4-6','7-9','10-12','13-15','16-18','19-21','22-24']
    print(totalPositiveSymps)
    print(dateStr)

    plt.plot(dateStr, totalPositiveSymps,
    label= "No of symptoms recognized per 3 days",  marker= "*", color='green', linestyle='dashed', linewidth = 3, markerfacecolor='blue',markersize=12) 
  
    # setting x and y axis range 
    plt.ylim(1,32) 
    plt.xlim(1,8) 
    # naming the x axis 
    plt.xlabel('Date intervals') 
    # naming the y axis 
    plt.ylabel('Number of positive symptoms') 
    plt.legend()
    # giving a title to my graph 
    plt.title('Positive predicted symptoms acc to date') 
    plt.savefig('plot1.png')
    report = str(pid)
    storage.child('charts1/{}'.format(report)).put('plot1.png')
    chart_url = storage.child('charts1/{}'.format(report)).get_url(None)
    data = {
            'chart_url':chart_url
        }
    res = charts1.document(pid).set(data)
    return data

@app.route('/charts2',methods=['POST'])
def charts2():
    r = request.json
    pid = r['pid']
    res = requests.get('http://34.93.231.96:5000/diagonized_medicines',json={'pid':'POC008'})
    data = res.json()
    doxyl = 0
    vist = 0
    xyzal = 0
    other = 0
    levoce = 0
    for d in data:
        x = data[d]['medicines']
        for i in x:
            if i['name'] == 'doxylamine':
                doxyl += i['dosage']
            elif i['name'] == 'vistaril':
                vist += i['dosage']
            elif i['name'] == 'Xyzal':
                xyzal += i['dosage']
            elif i['name'] == 'levocetirizili':
                levoce += i['dosage']
            else:
                other += i['dosage']


    x = [doxyl,vist,xyzal,levoce,other]
    y = ["doxylamine","vistaril",'Xyzal','levocetirizili','other']

    colors = ['r', 'y', 'g', 'b','m'] 
  
# plotting the pie chart 
    plt.pie(x, labels = y, colors=colors,  
    startangle=90, shadow = True,explode = (0.1,0.1,0.1,0.1,0),
    radius = 1.2, autopct = '%1.1f%%',pctdistance=1.1, labeldistance=1.3) ,
    handles = []
    for i, l in enumerate(y):
        handles.append(matplotlib.patches.Patch(color=plt.cm.Set3((i)/8.), label=l))
    plt.legend(handles,y, bbox_to_anchor=(0.9,1.025), loc="upper left")
    plt.title('Doasges or tablets taken for each medicine in a week\n\n') 
    plt.savefig('plot2.png')
    report = str(pid)
    storage.child('charts2/{}'.format(report)).put('plot2.png')
    chart_url = storage.child('charts2/{}'.format(report)).get_url(None)
    data = {
            'chart_url':chart_url
        }
    temp = pid+"pie"
    res = charts1.document(temp).set(data)
    return data

@app.route('/charts3',methods=['POST'])
def charts3():
    r = request.json
    pid = r['pid']
    print(pid)
    res = requests.get('http://34.93.231.96:5000/patient_details',json={'pid':pid})
    data = res.json()
    print(data)
    weight = data['weight']
    height = data['height']
    maze = io.imread('https://www.chartsgraphsdiagrams.com/HealthCharts/images/bmi-status-metric.png')
    cx = int(weight) #Kg
    cy = int(height) #cm

    patches = [Circle((cy, cx), radius=25, color='green')]
    fig, ax = plt.subplots(1)
    plt.axis('off')
    ax.imshow(maze)
    for p in patches:
        ax.add_patch(p)
    plt.title('BMI on the BMI Graph, Marker represents the BMI location.')
    plt.savefig('ans.png')
    report = str(pid)
    storage.child('charts3/{}'.format(report)).put('ans.png')
    chart_url = storage.child('charts3/{}'.format(report)).get_url(None)
    data = {
            'chart_url':chart_url
        }
    temp = pid+"bmi"
    res = charts1.document(temp).set(data)
    return data
    

    

if __name__ == '__main__':
    app.run(debug=True)


    # temp = http://f2aadc3f.ngrok.io/chart