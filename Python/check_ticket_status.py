import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from requests.exceptions import HTTPError
from lxml import etree


GMAIL_USERNAME = 'user@gmail.com'
GMAIL_SECRET = ''
FROM = GMAIL_USERNAME
TO = 'target@outlook.com'


def init_logging():
    logging.basicConfig(level=logging.DEBUG)


def get_raw_html(url):
    logging.info('Getting {0}...'.format(url))
    r = requests.get(url=url)

    if r.status_code != 200:
        raise HTTPError('Request to target URL failed.\n'
                        + str(r.text))

    return r.content


def get_smtp_client():
    return smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)


def check_ticket_status(raw_html):
    root = etree.HTML(raw_html)

    for e in root.cssselect('.fee-aside'):
        source = etree.tostring(e).decode(encoding='utf-8').lower()
        logging.info(source)
        if 'coming soon' not in source:
            raise Exception('Ticket sales started!')


if __name__ == '__main__':
    url = 'http://www.anime-expo.org/activity/concerts/'

    init_logging()
    smtp_client = get_smtp_client()
    smtp_client.login(GMAIL_USERNAME, GMAIL_SECRET)

    try:
        raw_html = get_raw_html(url)
        check_ticket_status(raw_html)
    except Exception as e:
        logging.exception(e)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Ticket Monitor Alert"
        msg['From'] = FROM
        msg['To'] = TO
        body = MIMEText(str(e))
        msg.attach(body)

        smtp_client.sendmail(from_addr=FROM, to_addrs=TO, msg=msg.as_string())
