#!/usr/bin/python

import sys
import time

import requests
from bs4 import BeautifulSoup

host = "192.168.8.1"
# port = "80"
port = None

if port:
    origin = f"http://{host}:{port}"
else:
    origin = f"http://{host}"

msg = sys.argv[1]

number = sys.argv[2]

time = time.strftime("%F %T", time.localtime())

payloadxml = (
    f'<?xml version="1.0" encoding="UTF-8"?>'
    f"<request>"
    f"<Index>-1</Index>"
    f"<Phones><Phone>{number}</Phone></Phones>"
    f"<Sca></Sca>"
    f"<Content>{msg}</Content>"
    f"<Length>{len(msg)}</Length>"
    f"<Reserved>1</Reserved>"
    f"<Date>2023-07-16 17:59:55</Date>"
    f"</request>"
)

url = f"{origin}/api/sms/send-sms"
referer = f"{origin}/html/smsinbox.html"

sendsms = requests.get(referer)

# Need to pass first csrf_token in html
soup = BeautifulSoup(sendsms.text, "html.parser")
token = [
    token["content"] for token in soup.findAll("meta", attrs={"name": "csrf_token"})
][0]

headers = {
    "__RequestVerificationToken": token,
}

r = requests.post(url, headers=headers, data=payloadxml, cookies=sendsms.cookies)
print(r.text)
