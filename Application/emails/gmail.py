 
from kivy.logger import Logger

SERVER = "imap.gmail.com"

import datetime
import email
import imaplib
import mailbox
import os
import base64
EMAIL_ACCOUNT = "your@gmail.com"
PASSWORD = "your password"





# result, data = mail.uid('search', None, "UNSEEN") # (ALL/UNSEEN)
# i = len(data[0].split())

# for x in range(i):
#     latest_email_uid = data[0].split()[x]
#     result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
#     # result, email_data = conn.store(num,'-FLAGS','\\Seen') 
#     # this might work to set flag to seen, if it doesn't already
#     raw_email = email_data[0][1]
#     raw_email_string = raw_email.decode('utf-8')
#     email_message = email.message_from_string(raw_email_string)

#     # Header Details
#     date_tuple = email.utils.parsedate_tz(email_message['Date'])
#     if date_tuple:
#         local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
#         local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
#     email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
#     email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
#     subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

#     # Body details
#     for part in email_message.walk():
#         body = part.get_payload(decode=True)
#         file_name = f"From:[{email_from}]To:[{email_to}]Date:[{local_message_date}]Subject:[{subject}]UID:[{str(x)}]"
#         output_file = open(file_name, 'w')
#         output_file.write(body.decode('utf-8'))
#         output_file.close()





class Emails(object):

    def __init__(self, server_name, inbox_type=None, mail_type=None):
        self.server_name = server_name
        self.items = None
        if not inbox_type:
            self.inbox_type = "inbox"

        if not mail_type:
            self.mail_type = "UNSEEN"
    
        self.data_dir = os.path.join(os.path.dirname(os.getcwd()), "user_data/emails/gmail")
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir) 




    def connect(self, username, password):
        self.mail_instance = imaplib.IMAP4_SSL(self.server_name)
        self.mail_instance.login(username, password)
        self.mail_instance.list()
        self.mail_instance.select(self.inbox_type)


    def fetch_email_ids(self):
        result, self.emails = self.mail_instance.uid('search', None, self.mail_type) # (ALL/UNSEEN)
        if result != "OK":
            Logger.error("Couldnt log into the mail server")
            raise Exception("Couldnt log into the mail server")

    def download_emails(self):
        """
        Downloding list of emails from the gmail server
        """

        self.fetch_email_ids()
        i = len(self.emails[0].split())
        #TODO: remove indexing on list
        for x in range(i):
            email_uid = self.emails[0].split()[x]
            email_from, email_to, subject, local_message_date, email_message = self.download_email(email_uid)
            self.save_email(email_uid, email_from, email_to, subject, local_message_date, email_message)
        return 


    def download_email(self, email_uid):
        """
        Download a particular email
        """
        # this might work to set flag to seen, if it doesn't already
        result, email_data = self.mail_instance.uid('fetch', email_uid, '(RFC822)')

        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        # Header Details
        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
        else:
            local_message_date = None

        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
        subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

        return email_from, email_to, subject, local_message_date, email_message


    def save_email(self, email_uid, email_from, email_to, subject, local_message_date, email_message):
        
        # Body details
        Logger.info(f"email_uid={email_uid}, email_from={email_from}, email_to={email_to}, subject={subject}, local_message_date={local_message_date}")
        for part in email_message.walk():
            body = part.get_payload(decode=True)
            file_name = "email_" + str(email_uid) + ".txt"

            j_file_name = f"From:[{email_from}]Date:[{local_message_date}]UID:[{str(email_uid)}Content-type:[{part.get_content_type()}]]"
            
            file_path = os.path.join(self.data_dir, file_name)
            Logger.info(f"J_Filepath {j_file_name}")


            output_file = open(file_path, 'w')
            if body:
                output_file.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(email_from, email_to,local_message_date, subject, base64.b64encode(body)))
            else:
                Logger.error(f"Body couldnt be parsed for {file_name}")
                output_file.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(email_from, email_to,local_message_date, subject, "Body coudlnt be parsed"))

            output_file.close()
        return 

if __name__ == "__main__":
    email_instance = Emails(SERVER)
    email_instance.connect("houzier.saurav@gmail.com", "Groot1234#")
    email_instance.download_emails()
