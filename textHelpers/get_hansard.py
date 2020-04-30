from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re


def GetHansard(date=None, members=None):
    if not date:
        date = datetime.strftime(datetime.now(), "%y-%m-%d")
    if not members:
        members = []
    statements = []
    base_url = "https://hansard.parliament.uk/html/Commons/%s/CommonsChamber" % date
    r = requests.get(base_url)
    hansard_html = r.text
    html_obj = BeautifulSoup(hansard_html, 'html.parser')
    content = html_obj.find_all(id=re.compile("contribution-.*"))
    for item in content:
        member = item.find("div", "member-container")
        if member:
            link = member.a.get("href")
            member_id = int(link.split('=')[-1])
            if member_id in members:
                text = ""
                statement = item.find("div", "contribution")
                # print(member_id)
                for para in statement.find_all("p"):
                    text += para.text
                statements.append([member_id, text])

    # print(statements)
    return statements
