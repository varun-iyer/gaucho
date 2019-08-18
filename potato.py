from bs4 import BeautifulSoup
import pickle
import re
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class ParseError(Exception):
    pass

class Section:
    instructor = ""
    days = ""
    time = ""
    space = 0
    time = ""
    enrlcd = 0
    location = ""
    max_ = 0

    def __init__(self, instructor, days, time, space, max_, location, enrlcd):
        self.instructor = instructor
        self.days = days
        self.time = time
        self.space = space
        self.max_ = max_
        self.location = location
        self.enrlcd = enrlcd

    def __init__(self, div):
        self.days = get_text(div.find_all('div', class_="col-lg-search-days")[0]).strip()
        self.time = get_text(div.find_all('div', class_="col-lg-search-time")[0]).strip()
        self.location = get_text(div.find_all('div', class_="col-lg-search-location")[0].find('a')).strip()
        self.instructor = get_text(div.find_all('div', class_="col-lg-search-instructor")[0].find('span')).strip()
        self.max_ = int(get_text(div.find_all('div', class_="col-lg-days")[0]).strip())
        self.enrlcd = int(get_text(div.find_all('div', class_="col-sm-pull-11")[0]).strip())
        try:
            self.space = int(get_text(div.find_all('div', class_="col-lg-search-space")[0]).strip())
        except ValueError:
            self.space = 0

         
    def __str__(self):
        return "{} {} taught by {} at {}: {} {} {}".format(self.days, self.time, self.instructor, self.location, self.space, self.max_, self.enrlcd)

class Lecture:
    instructor = ""
    days = ""
    time = ""
    location = ""
    space = 0
    max_ = 0
    enrlcd = 0
    sections = []

    def __str__(self):
        return "{} {} taught by {} at {}: {} {} {} with {} sections".format(self.days, self.time, self.instructor, self.location, self.space, self.max_, self.enrlcd, len(self.sections))

    def __init__(self, instructor, days, time, space, max_, enrlcd, location):
        self.instructor = instructor
        self.days = days
        self.time = time
        self.space = space
        self.max_ = max_
        self.enrlcd = enrlcd
        self.location = location
        self.sections = []

    def __init__(self, div):
        self.sections = []
        self.days = get_text(div.find_all('div', class_="col-lg-search-days")[0]).strip()
        self.time = get_text(div.find_all('div', class_="col-lg-search-time")[0]).strip()
        self.location = get_text(div.find_all('div', class_="col-lg-search-location")[0].find('a')).strip()
        self.instructor = get_text(div.find_all('div', class_="col-lg-search-instructor")[0].find('span')).strip()
        self.max_ = int(get_text(div.find_all('div', class_="col-lg-days")[0]).strip())
        self.enrlcd = int(get_text(div.find_all('div', class_="col-sm-pull-11")[0]).strip())
        try:
            self.space = int(get_text(div.find_all('div', class_="col-lg-search-space")[0]).strip())
        except ValueError:
            self.space = 0

        self.sections = []
        for section in div.find_all('div', class_='susbSessionItem'):
            self.add(Section(section))

    def add(self, section):
        self.sections.append(section)

class Course:
    dept = ""
    num = ""
    name = ""
    units = (0, 0)
    grading = ""
    lectures = []

    def __init__(self, dept, num, name):
        self.dept = dept
        self.num = num
        self.name = name
        self.lectures = []

    def __str__(self):
        return "{} {}: {}\n\t{} for {} units".format(self.dept, self.num,
            self.name, self.grading, self.units)

    def add(self, lecture):
        self.lectures.append(lecture)

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

def scrape_units(text):
    n = re.findall(r"\d\.\d", text)
    if len(n) == 2:
        return (float(n[0]), float(n[1]))
    else:
        return (float(n[0]), float(n[0]))

def scrape_grading(text):
    if "Letter" in text:
        return "LETTER"
    if "Pass" in text:
        return "P/NP"
    if "Optional" in text:
        return "OPT"

def get_text(div):
    return "".join(div.find_all(text=True, recursive=False))

def scrape(content):
    soup = BeautifulSoup((content), 'html.parser')
    headers = soup.find_all('div', class_='courseSearchHeader')
    info = soup.find_all('div', class_='row info')
    courses = []

    for ch in zip(headers, info):
        title_span = ch[0].find_all('span', class_='courseTitle')
        title_text = title_span[0].text
        course = scrape_title(title_text)

        grading_span = ch[0].find_all('span', class_='pr5')
        course.units = scrape_units(grading_span[0].text)
        course.grading = scrape_grading(grading_span[1].text)
        course.add(Lecture(ch[1]))
        courses.append(course)
    return courses

for arg in sys.argv[1:]:
	page = open(arg, "r").read()
	c = scrape(page)
	print("Finished {}".format(arg[arg.index("/") + 1:])
	pickle.dump(c, open("pickles/{}.p".format(arg[arg.index("/") + 1:]), "wb"))
