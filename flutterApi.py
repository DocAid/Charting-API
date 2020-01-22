from flask import Flask, redirect, url_for, request, jsonify,render_template
import os, io
import json
from PIL import Image
import PIL.Image
import requests
from google.cloud import vision
from google.cloud.vision import types
import base64
import time
import pyrebase
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from firebase_admin import credentials, firestore, initialize_app
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import pandas as pd
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
app = Flask(__name__)
reportsHandwritten = db.collection('HandWrittenReports')
reportsHand = db.collection('reportsHand')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
client = vision.ImageAnnotatorClient()
reportsHand = db.collection('reportsHand')


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

@app.route('/',methods=['GET','POST'])
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
        logo = "https://image.freepik.com/free-vector/doctor-character-background_1270-84.jpg"
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

@app.route('/hwr',methods=['POST'])
def hello():

    data = request.get_json()
    print(data['name'])
    print(data['image'])
    str1 = data['image']
    fh = open("imageToSave.png", "wb")
    fh.write(str1.decode('base64'))
    fh.close()


    with io.open('imageToSave.png', 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    docText = response.full_text_annotation.text
    print(docText)


    pages = response.full_text_annotation.pages
    for page in pages:
        for block in page.blocks:
            print('block confidence:', block.confidence)

            for paragraph in block.paragraphs:
                print('paragraph confidence:', paragraph.confidence)

                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])

                    print('Word text: {0} (confidence: {1}'.format(word_text, word.confidence))

                    for symbol in word.symbols:
                        print('\tSymbol: {0} (confidence: {1}'.format(symbol.text, symbol.confidence))

    
    return "Thanku"
if __name__ == '__main__':
    app.run(debug=True)