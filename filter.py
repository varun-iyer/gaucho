import sys
import pickle
from potato import *
import re
import requests
from urllib.parse import quote


def search(name):
    parts = name.split(" ")
    for n, p in reversed(list(enumerate(parts))):
        url = "http://www.identity.ucsb.edu/{}".format(quote('people_finder/?rs=search_person_records&rsargs=["person","{}"]&'.format(" ".join(parts[:n+1])), "&/?="))
        response = requests.get(url)
        emails = re.findall("[\w_\.]+@\w*\.?ucsb\.edu", response.content.decode("utf-8"))
        if len(emails) > 5:
            return ["TOO MANY RESULTS"]
        elif len(emails) > 0:
            return emails
    return ["NOT FOUND"]

for p in sys.argv[1:]:
    courses = pickle.load(open(p, "rb"))
    if len(courses) > 0:
        print("{} Department:".format(courses[0].dept))
    for c in courses:
        for l in c.lectures:
            if l.enrolled > 40 and (("8:00 AM" not in l.time) or c.dept == "S"):
                email = search(l.instructor)
                print("\t{} <{}>, {} {}: {} {} at {} with {} enrolled".format( \
                    l.instructor, email, c.name, c.num, l.days, l.time, \
                    l.location, l.enrolled))
    sys.stdout.flush()
