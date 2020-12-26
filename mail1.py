import smtplib
import ssl
import email
from socket import gaierror
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv

def menu():
    while 1:
        servertype = input("Which Server you want to use?: \n1. IITK\n2. Gmail\nEnter 1 or 2: ")
        if servertype in ["1","2"]:
            return servertype
        else:
            print("Enter right choice")
def send_mail(email, first_name, company_name):
    print("Sending Mail to",first_name,"<"+email+">")
    message = MIMEMultipart("alternative")
    message["Subject"] = "INVITATION TO STARTUP INTERNSHIP PROGRAM, IIT Kanpur"
    message["From"] = sender_name+" <"+sender_email+">"
    message["To"] = email
#    message["Cc"] = cc_mail
    text = """\
    Dear {name},
    
Greetings from Entrepreneurship Cell, IIT Kanpur!

I am writing to you on behalf of Start-up Internship Program (SIP), administrated by Entrepreneurship Cell IIT Kanpur. In this program, We invite various emerging startups from our country to provide internship opportunities to the students of IIT Kanpur.

ABOUT SIP IIT KANPUR

SIP has been running successfully for 11 years now. Ever since its launch, it has been striving to help emerging startups hire quality students from IIT Kanpur as summer interns and concurrently help our students gain some valuable work experience. SIP assists all the associated startups in hiring students, starting from resume forwarding to conducting interviews and/or tests.

I would like to take this opportunity to invite your Startup {company} to be a part of SIP 2020. You can hire summer interns for various profiles like Software Development, Analytics, Marketing, Designing, Operations, Data Science, Engineering, Business Development, Finance, Consulting etc. as per your requirements. The selection process will be at your discretion.
The recruitment will continue from January 2021 till April 2021 and the internship period will be from May to July 2021. The exact dates, however, will be decided by you.
I look forward to a positive reply from you and a long-lasting relationship with your organisation.

Regards,
{your_name}
Secretary, SIP
Entrepreneurship Cell
IIT Kanpur
M: {mobile}
    """
    html = """\
    <html>
      <body>
      <p>Dear {name},</p>
<p>Greetings from Entrepreneurship Cell, IIT Kanpur!</p>
<p>I am writing to you on behalf of <strong>Start-up Internship Program (SIP)</strong>, administrated by <strong>Entrepreneurship Cell IIT Kanpur</strong>. In this program, We invite various emerging startups from our country to provide internship opportunities to the students of IIT Kanpur.
</p><p><strong>ABOUT SIP IIT KANPUR</strong></p><p>
SIP has been running successfully for <strong>11 years</strong> now. Ever since its launch, it has been striving to help emerging startups hire quality students from IIT Kanpur as summer interns and concurrently help our students gain some valuable work experience. SIP assists all the associated startups in hiring students, starting from resume forwarding to conducting interviews and/or tests.
</p><p>I would like to take this opportunity to <strong>invite your Startup {company} to be a part of SIP 2020</strong>. You can <strong>hire summer interns</strong> for various profiles like Software Development, Analytics, Marketing, Designing, Operations, Data Science, Engineering, Business Development, Finance, Consulting etc. as per your requirements. The selection process will be at your discretion.
The recruitment will continue from January 2021 till April 2021 and the internship period will be from May to July 2021. The exact dates, however, will be decided by you.
I look forward to a positive reply from you and a long-lasting relationship with your organisation.
</p><p>
Regards,</p><p>
{your_name}<br />
Secretary, SIP<br />
Entrepreneurship Cell<br />
IIT Kanpur<br />
M: {mobile}</p>
      </body>
    </html>
    """
    part1 = MIMEText(text.format(name = first_name,company = company_name,your_name = sender_name,mobile = mobile_number),"plain")
    part2 = MIMEText(html.format(name = first_name,company = company_name,your_name = sender_name,mobile = mobile_number),"html")
    message.attach(part1)
    message.attach(part2)
    server.sendmail(sender_email,email,message.as_string())
#    server.sendmail(sender_email,cc_mail,message.as_string())
#    server.sendmail(sender_email,"*******@iitk.ac.in",message.as_string())
    print("Mail sent to", email)
    print("")
    


port = 465
file_name = input("Enter Your File Location: ")
sender_name = input("Enter Your Full Name: ")
mobile_number = input("Enter Your Mobile Number for Email Content Purpose: ")
servertype = menu()
if servertype == "1":
    smtp_server = "mmtp.iitk.ac.in"
    print("You are using IITK server. Go through this policy first: https://linux.cc.iitk.ac.in/lininfo/Email_account_security_poli.html\n")
    choice = input("Are you afraid of these policies? Consider changing the server(y/n): ")
    if choice=="y":
        print("\nYou are using Gmail Server. \nYou need to turn off 2-Step Verification here: https://myaccount.google.com/signinoptions/two-step-verification. \nAnd then allow less secure apps here: https://myaccount.google.com/lesssecureapps.")
        smtp_server = "smtp.gmail.com"
        print("\n******You have selected Gmail Server.*******")
    else:
        print("\n******You have selected IITK Server.********")
else:
    smtp_server = "smtp.gmail.com"
    print("You are using Gmail Server. \nYou need to turn off 2-Step Verification here: https://myaccount.google.com/signinoptions/two-step-verification. \nAnd then allow less secure apps here: https://myaccount.google.com/lesssecureapps. \nWhat am I doing? Am I insecuring my google account? Don't freak out. You are just gonna use them yourself.\nAnd then reset the settings after your work.")
    choice = input("Still feeling insecure. Consider changing your server(y/n): ")
    if choice=="y":
        smtp_server = "mmtp.iitk.ac.in"
        print("\nYou are using IITK server. Go through this policy first: https://linux.cc.iitk.ac.in/lininfo/Email_account_security_poli.html\n")
        
        print("\n*******You have selected IITK Server.*******")
    else:
        print("\n*******You have selected Gmail Server.*******")

sender_email = input("Enter your email: ")
password = input("Type your password and press enter: ")
cc_mail = "sip@ecelliitk.com"


context = ssl.create_default_context()
try:
    #send your message with credentials specified above
    print("Connecting to server...")
    with smtplib.SMTP_SSL(smtp_server, port,context=context) as server:
        print("Authenticating...")
        server.login(sender_email, password)
        count = 0
        print("\n**********Sending Mail*******************")
        with open(file_name) as file:
          reader = csv.reader(file)
          for company,name,email in reader:
            count+=1
            first_name = name.strip().split()[0]
            send_mail(email, first_name, company)
        print("***Successfully sent",count,"Emails***")
except (gaierror, ConnectionRefusedError):
    print('Failed to connect to the server. Bad connection settings?')
except smtplib.SMTPServerDisconnected:
    print('Failed to connect to the server. Wrong user/password?')
except smtplib.SMTPException as e:
    print('SMTP error occurred: ' + str(e))
