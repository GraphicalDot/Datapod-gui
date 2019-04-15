 

SERVER = "imap.gmail.com"

import datetime
import email
import imaplib
import mailbox
import os
import base64
EMAIL_ACCOUNT = "your@gmail.com"
PASSWORD = "your password"



import coloredlogs, verboselogs, logging
verboselogs.install()
coloredlogs.install()
logger = logging.getLogger(__name__)



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
            self.mail_type = "ALL"
    
        self.email_dir = os.path.join(os.path.dirname(os.getcwd()), "user_data/mails/gmail/emails")
        if not os.path.exists(self.email_dir):
            os.makedirs(self.email_dir) 

        self.image_dir = os.path.join(os.path.dirname(os.getcwd()), "user_data/mails/gmail/images")
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir) 

        self.pdf_dir = os.path.join(os.path.dirname(os.getcwd()), "user_data/mails/gmail/pdfs")
        if not os.path.exists(self.pdf_dir):
            os.makedirs(self.pdf_dir) 
        logger.info("App intiation been done")

    def connect(self, username, password):
        self.mail_instance = imaplib.IMAP4_SSL(self.server_name)
        self.mail_instance.login(username, password)
        self.mail_instance.list()
        self.mail_instance.select(self.inbox_type)
        logger.info("COnnected successffuly")


    def fetch_email_ids(self):
        result, self.emails = self.mail_instance.uid('search', None, self.mail_type) # (ALL/UNSEEN)
        if result != "OK":
            logger.error("Couldnt log into the mail server")
            raise Exception("Couldnt log into the mail server")

    def download_emails(self):
        """
        Downloding list of emails from the gmail server
        """
        logger.info("Executing download emails")

        self.fetch_email_ids()
        i = len(self.emails[0].split())
        logger.info(f"NUmber of emails is {i}")

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
        logger.info(f"email_uid={email_uid}, email_from={email_from}, email_to={email_to}, subject={subject}, local_message_date={local_message_date}")
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                logger.warning(f"CONTENT Dispostion is {part.get('Content-Disposition')}")
                continue


            body = part.get_payload(decode=True)
            content_type= part.get_content_type()
            file_name = "email_" + str(email_uid) + ".txt"

            j_file_name = f"From:[{email_from}]Date:[{local_message_date}]UID:[{str(email_uid)}Content-type:[{content_type}]]"
            
            file_path = os.path.join(self.email_dir, file_name)
            logger.info(f"J_Filepath {j_file_name}")
            
            
            attachment_name = part.get_filename()
            if attachment_name:
                if content_type == "application/pdf":
                    with open(os.path.join(self.pdf_dir, attachment_name), "wb") as f:
                        f.write(part.get_payload(decode=True))

                if content_type.startswith("image"):
                    with open(os.path.join(self.image_dir, attachment_name), "wb") as f:
                        f.write(part.get_payload(decode=True))
 
            
            logger.info(f"Attachment in the email name is  {attachment_name}")

            output_file = open(file_path, 'w')
            if body:
                output_file.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(email_from, email_to,local_message_date, subject, base64.b64encode(body)))
            else:
                logger.error(f"Body couldnt be parsed for {file_name}")
                output_file.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(email_from, email_to,local_message_date, subject, "Body coudlnt be parsed"))

            output_file.close()
        return 

if __name__ == "__main__":
    logger.info("App started")
    email_instance = Emails(SERVER)
    email_instance.connect("dummy.houzier.saurav@gmail.com", "Groot1234#")
    email_instance.download_emails()
    logger.info("App Ended")
