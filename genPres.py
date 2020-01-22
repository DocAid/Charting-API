import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
 
doc = SimpleDocTemplate("form_letter1.pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
Story=[]
logo = "hi.jpg"
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


ptext = '<font size=12>%s</font>' % docText
Story.append(Paragraph(ptext, styles["Normal"]))

for part in address_parts:
    ptext = '<font size=12>%s</font>' % part.strip()
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