import os
import imapclient
import pyzmail

# Email login details
EMAIL_ADDRESS = os.environ['server_email']
EMAIL_PASSWORD = os.environ['server_passwd']

# Connect to IMAP and login
imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
imapObj.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
imapObj.select_folder('INBOX', readonly=False)

# Search for all unread emails
unread_emails = imapObj.search(['UNSEEN'])


for email_id in unread_emails:
    raw_message = imapObj.fetch([email_id], ['BODY[]'])
    message = pyzmail.PyzMessage.factory(raw_message[email_id][b'BODY[]'])

    # Extract the subject and body
    subject = message.get_subject()
    body = message.text_part.get_payload().decode(message.text_part.charset)

    # Here you can parse your data
    # For example, let's just print the body
    print(f"{subject}")

    # Mark the email as read (optional)
    #imapObj.store(email_id, '+FLAGS', '\\Seen')

imapObj.logout()
