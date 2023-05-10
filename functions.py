from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


#Function to make files with the data collected
def make_Files(option, df):

    #Declaring the list to interact with the save procedure
    pathList = ["Tables-Users", "Tables-Clients", "Tables-Stock", "Tables-Payments"]
    SheetList = ["Usuários", "Clientes", "Estoque", "Pagamentos"]
    
    #Saving files in the corresponding folder
    time = datetime.now()
    reportName = time.strftime("%d-%m-%Y_%H#%M#%S")
    df.to_csv(os.path.abspath(os.getcwd()) + "\\{}\\CSV_{}.csv".format(pathList[option], reportName), index=False, header=True)
    df.to_excel(os.path.abspath(os.getcwd()) + "\\{}\\Excel_{}.xlsx".format(pathList[option], reportName), sheet_name="{}".format(SheetList[option]))

    return reportName


#Function to send email with the corresponding report
def send_Email(option, product, reportName, userEmail):

    #Declaring the list to interact with the sending procedure
    pathList = ["Tables-Users", "Tables-Clients", "Tables-Stock", "Tables-Payments"]

    #Starting smtp server
    server = smtplib.SMTP("smtp.gmail.com", "587")
    server.ehlo()
    server.starttls()
    server.login("rickpincelli@gmail.com", "fqydnfdnizsvukdo")

    #Building the email
    body = "<b>Olá, tudo bem? Segue em anexo o relatório. O primeiro no formato 'XLSX' e o segundo no formato 'CSV'.</b>"
    emailOBJ = MIMEMultipart()
    emailOBJ["From"] = "rickpincelli@gmail.com"
    emailOBJ["To"] = userEmail
    emailOBJ["Subject"] = "Relatórios - {}".format(product)
    emailOBJ.attach(MIMEText(body, "html"))

    #Open XLSX file in read mode and binary
    XLSXFilePath = os.path.abspath(os.getcwd()) + "\\{}\\Excel_{}.xlsx".format(pathList[option], reportName)
    XLSXAttchment = open(XLSXFilePath, "rb")
    #Read the file and convert to Base64
    att = MIMEBase("application", "octet-stream")
    att.set_payload(XLSXAttchment.read())
    encoders.encode_base64(att)
    #Adding a header and closing the XLSX file
    att.add_header("Content-Disposition", f"attachment; filename=Excel_{reportName}.xlsx")
    XLSXAttchment.close()
    emailOBJ.attach(att)

    #Open CSV file in read mode and binary
    CSVFilePath = os.path.abspath(os.getcwd()) + "\\{}\\CSV_{}.csv".format(pathList[option], reportName)
    CSVAttchment = open(CSVFilePath, "rb")
    #Read the file and convert to Base64
    att = MIMEBase("application", "octet-stream")
    att.set_payload(CSVAttchment.read())
    encoders.encode_base64(att)
    #Adding a header and closing the CSV file
    att.add_header("Content-Disposition", f"attachment; filename=CSV_{reportName}.csv")
    CSVAttchment.close()
    emailOBJ.attach(att)

    #Sending the email
    server.sendmail(emailOBJ["From"], emailOBJ["To"], emailOBJ.as_string())
    server.quit()

    return