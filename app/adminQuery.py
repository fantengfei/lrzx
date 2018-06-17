"""
    adminQuery
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

# from autoscript import script
from db.sql import Database
import common

def verify_user(username, password):
    db = Database('verify_user')
    re = db.query("""select password from account where number='%s' and status = 1 """, (username,), True)
    if re and re.has_key('password') and re['password'] == common.md5(password):
        return True

    return False




def analysisURL(url):
    import requests
    from readability import Document
    import json

    html = requests.get(url)

    article = Document(html.text).summary()
    title = Document(html.text).short_title()


    data = {"content": article, "title": title}
    return json.dumps(data)



