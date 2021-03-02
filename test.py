import smtplib
import csv
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass


class mail:

    __email = None
    __password = None

    def __init__(self):
        self.__email = self.__email = input("Enter you gmail id: ")
        self.__password = getpass.getpass(prompt="Enter your password: ")
        s = smtplib.SMTP(host='smtp.gmail.com', port=587, timeout=300)
        s.starttls()
        try:
            s.login(self.__email, self.__password)
            print("Login Successfull")
            s.quit()
        except:
            print("Login failed. Try Again")
            return

    def mailer(self, csv_reader, message_template):
        s = smtplib.SMTP(host='smtp.gmail.com', port=587, timeout=300)
        s.starttls()
        s.login(self.__email, self.__password)
        l, fc = 0, 0
        for lines in csv_reader:
            msg = MIMEMultipart()
            l += 1
            message = message_template.substitute(
                name=lines[0], section=lines[3], ID=lines[4])

            msg['From'] = self.__email
            msg['To'] = lines[2]
            msg['Subject'] = "Add your own subject"
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
        s.quit()
        if (fc > 0):
            print("failed count: ", fc)
            print("Mails send up to Line No. in the CSV file: ", (l-fc))


def read_template(filename):
    with open(filename, encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def makesublist(lst, n):
    sub = []
    result = []
    for i in lst:
        sub += [i]
        if len(sub) == n:
            result += [sub]
            sub = []
    if sub:
        result += [sub]
    return result


def main():

    m = mail()
    message_template = read_template('template.html')

    with open("details.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        csv_reader = list(csv_reader)
        submails = makesublist(csv_reader, 10)
        for sublist in submails:
            m.mailer(sublist, message_template)


if __name__ == '__main__':
    main()
