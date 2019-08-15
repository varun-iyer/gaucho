from bs4 import BeautifulSoup
import re
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class ParseError(Exception):
    pass

class Course:
    dept = ""
    num = ""
    name = ""
    def __init__(self, dept, num, name):
        self.dept = dept
        self.num = num
        self.name = name

    def __str__(self):
        return "{} {}: {}".format(self.dept, self.num, self.name)
         
page = open("scrape.html", "r").read()

def scrape_title(text):
    dept = re.findall("^[A-Z]+\s", text)
    if len(dept) == 1:
        dept = dept[0].strip()
    else:
        raise ParseError("Did not find dept! {}".format(text))
    num = re.findall("\s\d+\w*\s", text)
    if len(num) == 1:
        num = num[0].strip()
    else:
        raise ParseError("Did not find dept! {}".format(text))
    idx = text.index(num) + len(num)
    name = text[idx:].strip()
    name = re.sub("^\W+", "", name)
    name = re.sub("\W+$", "", name)
    return Course(dept, num, name)

def scrape(content):
    soup = BeautifulSoup((content), 'html.parser')
    course_html = soup.find_all('div', class_='courseSearchItem')
    course_html = list(zip(course_html[0::2], course_html[1::2]))
    courses = []

    for ch in course_html:
        title_span = ch[0].find_all('span', class_='courseTitle')
        if len(title_span) != 1:
            eprint("Did not find title in {}".format(ch[0]))
            continue
        title_text = title_span[0].text
        courses.append(scrape_title(title_text))
        
        grading_span = ch[0].find_all('span', class_='pr5'))
        if len(grading_span) != 2:
            eprint("Did not find grading info in {}".format(ch[0]))
            continue
         
    print([str(c) for c in courses])

scrape(page)
