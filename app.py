import matplotlib.pyplot as plt
import matplotlib
from skimage import io
from matplotlib.patches import Arrow, Circle
import pdfkit
from flask import Flask, redirect, url_for, request, jsonify,render_template
import os
from PIL import Image
import PIL.Image
import requests
from google.cloud import vision
import time
import pyrebase
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from firebase_admin import credentials, firestore, initialize_app
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import pandas as pd
import seaborn as sns

app = Flask(__name__)
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()

reportsHandwritten = db.collection('HandWrittenReports')
reportsHand = db.collection('reportsHand')
client = vision.ImageAnnotatorClient()
reportsHand = db.collection('reportsHand')

serverAddr = 'http://69b08d09.ngrok.io'


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
reportsHand = db.collection('reportsHand')
charts1 = db.collection('charts1')
charts2 = db.collection('charts2')

docCharts = db.collection('docCharts')


@app.route('/', methods=['GET','POST'])
def index():
    print("hi")
    if request.method == 'POST':
        data = request.json   
        image = request.files['file']
        pil_image = PIL.Image.open(image)
        a1 = pil_image.save("hi.jpg")
        # print(data.get_json)
        print(type(data)) 
        print(data)

        with io.open('hi.jpg', 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)
        response = client.document_text_detection(image=image)
        docText = response.full_text_annotation.text
        print(docText)
        print(type(docText))

        doc = SimpleDocTemplate("reportHand.pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
        Story=[]
        logo = "./doc.jpg"
        magName = "Pythonista"
        issueNum = 12
        subPrice = "99.00"
        limitedDate = "03/05/2010"
        freeGift = "tin foil hat"
        
        formatted_time = time.ctime()
        full_name = "DR Pramila Nair"
        address_parts = ["Government Medical College", "Aurangabaad"]
        
        im = Image(logo, 2*inch, 2*inch)
        Story.append(im)
        
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        ptext = '<font size=12>%s</font>' % formatted_time
        
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        # Create return address
        ptext = '<font size=12>%s</font>' % full_name
        Story.append(Paragraph(ptext, styles["Normal"]))

        
        for part in address_parts:
            ptext = '<font size=12>%s</font>' % part.strip()
            Story.append(Paragraph(ptext, styles["Normal"]))   
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))

        ptext = '<font size=16>%s</font>' % docText
        Story.append(Paragraph(ptext, styles["Normal"]))


        Story.append(Spacer(1, 12))
        # ptext = '<font size=12>Dear %s:</font>' % full_name.split()[0].strip()
        # Story.append(Paragraph(ptext, styles["Normal"]))
        # Story.append(Spacer(1, 12))


        
        # ptext = '<font size=12>Thank you for the storing yoir digital prescrption. %s \
        #         You will receive %s issues at the excellent introductory price of $%s. Please respond by\
        #         %s to start receiving your subscription and get the following free gift: %s.</font>' % (magName, 
        #                                                                                                 issueNum,
        #                                                                                                 subPrice,
        #                                                                                                 limitedDate,
        #                                                                                                 freeGift)
        # Story.append(Paragraph(ptext, styles["Justify"]))
        # Story.append(Spacer(1, 12))
        
        
        ptext = '<font size=12>Please take the dosages in the required format. For any furthur queries contact the doctor.</font>'
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))
        ptext = '<font size=12>Sincerely,</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 48))
        im = Image("https://firebasestorage.googleapis.com/v0/b/docaid-api.appspot.com/o/img2.png?alt=media&token=18f4aa32-badf-4104-9e85-693dd8a96561", 2*inch, 2*inch)
        Story.append(im)
        ptext = '<font size=12>Dr Pramila Nair</font>'
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        doc.build(Story)
        storage.child('reportsHand').put('reportHand.pdf')

    return "Hello World"                          

@app.route('/getHandWritten')
def nimish():
    pdf_url = storage.child('reportsHand').get_url(None)
    data = {
            'pdf_url':pdf_url
    }
    res = reportsHand.document("reportHand").set(data)
    data = reportsHand.document("reportHand").get()
    print(data)
    print(data.to_dict())
    return jsonify(data.to_dict())    


@app.route('/rg',methods=['POST'])
def genPdf():
    if request.method == 'POST':
        data = request.json
        age = data['age']
        pid = data['pid']
        dosages = data['dosages']
        bmi = data['bmi']
        img1 = 'https://firebasestorage.googleapis.com/v0/b/docaid-api.appspot.com/o/img1.jpg?alt=media&token=63ba5fe0-d6a7-42e9-8644-129c85725845'
        img2 = 'https://images.shiksha.com/mediadata/images/1572338222phpspG6Yo.png'
        x = render_template('r.html',pid=pid,age=age,bmi=bmi,dosages=dosages,img1=img1,img2=img2)
        print(type(x))
        print(x)
        pdfkit.from_string(x,'report1.pdf')
        report = str(pid)
        storage.child('reportsPdf/{}'.format(report)).put('report1.pdf')
        pdf_url = storage.child('reportsPdf/{}'.format(report)).get_url(None)
        data = {
            'pdf_url':pdf_url,
            'patient_id':pid,
            'status': True
        }
        res = reports.document(pid).set(data)
        return pdf_url

@app.route('/rg1',methods=['POST'])
def genPdf1():
    pdf_url = storage.child('reportsHand').get_url(None)
    data = {
        'pdf_url':pdf_url
    }
    res = reportsHand.document("reportHand").set(data)
    data = reportsHand.document("reportHand").get()
    print(data)
    print(data.to_dict())
    return jsonify(data.to_dict())

@app.route('/sendReportToDB',methods=['POST'])
def getReport():
    requestData = request.json
    pid = requestData['pid']
    data = reports.document(pid).get()
    print(data)
    print(data.to_dict())
    return jsonify(data.to_dict())



@app.route('/charts1',methods=['POST'])
def chart1():
    r = request.json
    pid = r['pid']
    print(pid)
    res = requests.get(serverAddr + '/keywords',json={'pid':'POC008'})
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
    res = requests.get(serverAddr + '/diagonized_medicines',json={'pid':'POC008'})
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
    plt.clf()
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
    res = requests.get(serverAddr + '/patient_details',json={'pid':pid})
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
    plt.clf()
    report = str(pid)
    storage.child('charts3/{}'.format(report)).put('ans.png')
    chart_url = storage.child('charts3/{}'.format(report)).get_url(None)
    data = {
            'chart_url':chart_url
        }
    temp = pid+"bmi"
    res = charts1.document(temp).set(data)
    return data
    

@app.route('/docChart1')
def docChart1():
    x = ['11th','12th','13th','14th','15th','16th','17th','18th','19th','20th']
    y = [10,6,30,23,43,7,9,28,35,11]

    plt.plot(x,y,
    label= "No of patients visited per day",  marker= "o", color='green', linestyle='dashed', linewidth = 3, markerfacecolor='blue',markersize=12) 
    plt.xlabel('Date') 
    plt.ylabel('Number of patients') 
    plt.legend()
    plt.title("No of patients visited per day") 
    plt.savefig('docChart1.png')
    plt.clf()
    storage.child('docCharts/{}'.format("plot1")).put('docChart1.png')
    chart_url = storage.child('docCharts/{}'.format("plot1")).get_url(None)
    print(chart_url)
    data = {
            'chart_url':chart_url
        }
    res = docCharts.document("plot1").set(data)
    return data


@app.route('/docChart2')
def docChart2():
    
    doctor_df1 = pd.read_csv("data1.csv")
    sns.set(style="darkgrid")
    ax = sns.countplot(x="week1", data=doctor_df1,hue="severity",palette="Set1")
    ax.set(title="No of patients per day according to severity", xlabel="Date", ylabel="Number of patients")
    plt.savefig('docChart2.png')
    plt.clf()
    storage.child('docCharts/{}'.format("plot2")).put('docChart2.png')
    chart_url = storage.child('docCharts/{}'.format("plot2")).get_url(None)
    print(chart_url)
    data = {
            'chart_url':chart_url
        }
    res = docCharts.document("plot2").set(data)
    return data

@app.route('/docChart3')
def docChart3():
    x = ["Jan","Feb","March","April","May","June"]
    y = [40000,32000,34000,42000,26000,45000]

    plt.plot(x,y,
    label= "Earnings per Month",  marker= "o", color='blue', linestyle='solid', linewidth = 3, markerfacecolor='blue',markersize=12) 
    plt.xlabel('Month') 
    plt.ylim(0,50000)
    plt.ylabel('Earnings (in Rupees)') 
    plt.legend()
    plt.title("Earnings per month") 

    plt.plot(x,y,
    label= "Salary per month",  marker= "o", color='green', linestyle='dashed', linewidth = 3, markerfacecolor='blue',markersize=12) 
    plt.savefig('docChart3.png')
    plt.clf()
    storage.child('docCharts/{}'.format("plot3")).put('docChart3.png')
    chart_url = storage.child('docCharts/{}'.format("plot3")).get_url(None)
    print(chart_url)
    data = {
            'chart_url':chart_url
        }
    res = docCharts.document("plot3").set(data)
    return data


@app.route('/docChart4')
def docChart4():
    # Data to plot
    labels = 'Diarrohea', 'Fever', 'Allergy', 'Injury'
    sizes = [17,40,9,15]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0, 0)  # explode 1st slice


    plt.title("Patients with different diseases")
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal') 
    plt.savefig('docChart4.png')
    plt.clf()
    storage.child('docCharts/{}'.format("plot4")).put('docChart4.png')
    chart_url = storage.child('docCharts/{}'.format("plot4")).get_url(None)
    print(chart_url)
    data = {
            'chart_url':chart_url
        }
    res = docCharts.document("plot4").set(data)
    return data


if __name__ == '__main__':
    app.run(port=8888, debug=True)
