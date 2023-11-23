import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
try:
    msg = MIMEMultipart()
    msg['From'] = 'refit_dev@sidneyshapiro.com'
    msg['To'] = 'refit_dev@sidneyshapiro.com'
    msg['Subject'] = 'Welcome to REFit!'
    
    # Read the HTML content from your file
    with open("email_template/my_templates/welcome_template.html", "r") as file:
        html = file.read()

    # Attach the HTML content
    msg.attach(MIMEText(html, 'html'))

    email_text = msg.as_string()
        
    email_text = msg.as_string()
    #Send an email to the email address typed in the form.
    smtpObj = smtplib.SMTP_SSL('mail.sidneyshapiro.com', 465)  # Using SMTP_SSL for secure connection
    smtpObj.login('refit_dev@sidneyshapiro.com', 'P7*XVEf1&V#Q')  # Log in to the server
    smtpObj.sendmail('refit_dev@sidneyshapiro.com', 'refit_dev@sidneyshapiro.com', email_text)
    smtpObj.quit()  # Quitting the connection
    
    print("Email sent successfully!")
except Exception as e:
    print("Oops, something went wrong: ", e)