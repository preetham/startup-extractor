#! /usr/bin/env python3
# ~*~ utf-8 ~*~

import mailbox
from urllib.parse import unquote
import bs4
import re
import datefinder


def get_html_text(html):
    try:
        return bs4.BeautifulSoup(html, 'lxml').body.get_text('', strip=True)
    except AttributeError: # message contents empty
        return None

class GmailMboxMessage():
    def __init__(self, email_data):
        if not isinstance(email_data, mailbox.mboxMessage):
            raise TypeError('Variable must be type mailbox.mboxMessage')
        self.email_data = email_data

    def parse_email(self):
        email_labels = self.email_data['X-Gmail-Labels']
        email_date = self.email_data['Date']
        email_from = self.email_data['From']
        email_to = self.email_data['To']
        email_subject = self.email_data['Subject']
        email_text = self.read_email_payload() 

    def read_email_payload(self):
        email_payload = self.email_data.get_payload()
        if self.email_data.is_multipart():
            email_messages = list(self._get_email_messages(email_payload))
        else:
            email_messages = [email_payload]
        return [self._read_email_text(msg) for msg in email_messages]

    def _get_email_messages(self, email_payload):
        for msg in email_payload:
            if isinstance(msg, (list,tuple)):
                for submsg in self._get_email_messages(msg):
                    yield submsg
            elif msg.is_multipart():
                for submsg in self._get_email_messages(msg.get_payload()):
                    yield submsg
            else:
                yield msg

    def _read_email_text(self, msg):
        content_type = 'NA' if isinstance(msg, str) else msg.get_content_type()
        encoding = 'NA' if isinstance(msg, str) else msg.get('Content-Transfer-Encoding', 'NA')
        if 'text/plain' in content_type and 'base64' not in encoding:
            msg_text = msg.get_payload()
        elif 'text/html' in content_type and 'base64' not in encoding:
            msg_text = get_html_text(msg.get_payload())
        elif content_type == 'NA':
            msg_text = get_html_text(msg)
        else:
            msg_text = None
        return (content_type, encoding, msg_text)


def cleanup(raw_text):
    text = re.sub('=(\r\n)', '', raw_text)
    text = re.sub(r'=([0-9][A-Z])', r'%\1', text)
    text = re.sub(r'=[A-Z][0-9]=(.){2,5}', '', text)
    text = unquote(text)
    return text

mbox_obj = mailbox.mbox('./raw-data/AngelList.mbox')

num_entries = len(mbox_obj)

for idx, email_obj in enumerate(mbox_obj):
    email_data = GmailMboxMessage(email_obj)
    email_data.parse_email()
    data = email_data.read_email_payload()
    if len(data) > 0:
        raw_content = data[0][2]
        clean_content = cleanup(raw_text=raw_content)
        dates = datefinder.find_dates(clean_content, source=True)
        article_date = next(dates)
        with open('./parsed-data/'+ article_date[1] + '.txt', 'w') as f:
            f.write(clean_content)
