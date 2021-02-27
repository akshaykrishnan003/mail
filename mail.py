import smtplib
import csv
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def read_template(filename):
    with open(filename, encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def main():
    fc = 0
    message_template = read_template('template.html')
    MY_ADDRESS = '<yourmailid>'
    PASSWORD = '<yourpassword>'
# set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587, timeout=300)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    with open("details.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
  # the below statement will skip the first row
        next(csv_reader)
        l = 0
        for lines in csv_reader:
            msg = MIMEMultipart()
            l += 1
            # print(msg)  # create a message
# add in the actual person name to the message template
            message = message_template.substitute(
                PERSON_NAME=lines[0], section=lines[3], ID=lines[4])
            # print(message)
# setup the parameters of the message
            msg['From'] = MY_ADDRESS
            msg['To'] = lines[2]
            msg['Subject'] = "IEEE PES DAY 2021: IEEE PES Student Branch Chapter Ambassadors Selection"
# add in the message body
            msg.attach(MIMEText(message, 'html'))
# send the message via the server set up earlier.

            try:
                s.send_message(msg)
                print("success: ", lines[2])
            except:
                fc += 1
                print("failed mail: ", lines[2])

            del msg

 # Terminate the SMTP session and close the connection
    print("failed count: ", fc)
    print("Check line: ", (l-fc)+1)
    s.quit()


if __name__ == '__main__':
    main()
