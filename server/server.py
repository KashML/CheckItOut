import os
import time
import imapclient
import pyzmail

# fzf for bashrc
# [ -f ~/.fzf.bash ] && source ~/.fzf.bash


# Email login details
EMAIL_ADDRESS = os.environ['server_email']
EMAIL_PASSWORD = os.environ['server_passwd']


class ServerController:

    def __init__(self) -> None:
        
        self.con_status: bool = False


    def establish_connection(self) -> bool:
        """Tries to establish connection"""
        try:
            self.client: imapclient = imapclient.IMAPClient('imap.gmail.com', ssl=True)
            self.client.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print("Login Successful")
            self.con_status = True

            return True
        except Exception as exec: 
            self.con_status = False
            print(f"Failed to Establish Connection :: {exec}")
            
            return False
    
    def get_inbox_all(self) -> list:
        """Get all email"""
        self.client.select_folder('INBOX', readonly=False)
        emails = self.client.search(['ALL'])
        
        return emails

    def get_inbox_unseen(self) -> list:
        """Get all unseen emails"""

        self.client.select_folder('INBOX', readonly=False)
        emails = self.client.search(['UNSEEN'])

        return emails
    
    def get_data(self,is_all: bool = False) -> list:
        """Get Email Content"""

        s_time = time.time()

        if self.con_status is not True:
            raise RuntimeError("Connection not established. Please call establish_connection() or check connection.")

        data = []
        emails = self.get_inbox_all() if is_all is True else self.get_inbox_unseen()
    

        for i, email_id in enumerate(emails):
            print(f"Parsing {i + 1} email out of {len(emails)} ...")
            
            raw_message = self.client.fetch([email_id], ['BODY[]'])
            message = pyzmail.PyzMessage.factory(raw_message[email_id][b'BODY[]'])

            # Extract the subject and body
            subject = message.get_subject()
            body = message.text_part.get_payload().decode(message.text_part.charset)

            data.append((subject, body))

        print(f"Total Time Taken : {time.time() - s_time}")
        return data
  
    def close(self)-> None:
        self.client.logout()



if __name__ == "__main__":

    S = ServerController()
    S.establish_connection()
    S.get_data(is_all=True)
