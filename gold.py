import requests
from lxml import html

categories = [
     "ANTH ",
     "ART  ",
     "ARTHI",
     "ARTST",
     "AS AM",
     "ASTRO",
     "BIOL ",
     "BMSE ",
     "BL ST",
     "CH E ",
     "CHEM ",
     "CH ST",
     "CHIN ",
     "CLASS",
     "COMM ",
     "C LIT",
     "CMPSC",
     "CMPTG",
     "CNCSP",
     "DANCE",
     "DYNS ",
     "EARTH",
     "EACS ",
     "EEMB ",
     "ECON ",
     "ED   ",
     "ECE  ",
     "ENGR ",
     "ENGL ",
     "ESM  ",
     "ENV S",
     "ESS  ",
     "ES   ",
     "FEMST",
     "FAMST",
     "FR   ",
     "GEN S",
     "GEOG ",
     "GER  ",
     "GPS  ",
     "GLOBL",
     "GRAD ",
     "GREEK",
     "HEB  ",
     "HIST ",
     "INT  ",
     "ITAL ",
     "JAPAN",
     "KOR  ",
     "LATIN",
     "LAIS ",
     "LING ",
     "LIT  ",
     "MARSC",
     "MATRL",
     "MATH ",
     "ME   ",
     "MAT  ",
     "ME ST",
     "MES  ",
     "MS   ",
     "MCDB ",
     "MUS  ",
     "MUS A",
     "PHIL ",
     "PHYS ",
     "POL S",
     "PORT ",
     "PSY  ",
     "RG ST",
     "RENST",
     "RUSS ",
     "SLAV ",
     "SOC  ",
     "SPAN ",
     "SHS  ",
     "PSTAT",
     "TMP  ",
     "THTR ",
     "WRIT "
]

viewstates = open("viewstate.dat", "r").readlines()
login_vs = viewstates[0].strip()
find_vs = viewstates[1].strip()
credentials = open("credentials.dat", "r").readlines()
username = viewstates[0].strip()
password = viewstates[1].strip()
login = {
    "__LASTFOCUS":"",
    "__VIEWSTATE":login_vs,
    "__VIEWSTATEGENERATOR":"00732C32",
    "__EVENTTARGET":"",
    "__EVENTARGUMENT":"",
    "__EVENTVALIDATION":"/wEdAAdbKm4OU/lsarSPEWzw3woTFPojxflIGl2QR/+/4M+LrK6wLDfR+5jffPpLqn7oL3ttZruIm/YRHYjEOQyILgzL2Nu6XIik3f0iXq7Wqnb39/ZNiE/A9ySfq7gBhQx160NmmrEFpfb3YUvL+k7EbVnKgIKH2XlDUw30P837MyfVDMpYxIk=",
    "ctl00$pageContent$userNameText":username,
    "ctl00$pageContent$passwordText":password,
    "ctl00$pageContent$loginButton":"Login",
    "ctl00$pageContent$PermPinLogin$userNameText":"",
    "ctl00$pageContent$PermPinLogin$passwordText":""
}

find = {
    "__EVENTTARGET":"",
    "__EVENTARGUMENT":"",
    "__LASTFOCUS":"",
    "__VIEWSTATE":find_vs,
    "__VIEWSTATEGENERATOR":"B22B3C44",
    "ctl00$pageContent$quarterDropDown":"20194",
    "ctl00$pageContent$departmentDropDown":categories[0],
    "ctl00$pageContent$subjectAreaDropDown":"",
    "ctl00$pageContent$courseNumberTextBox":"",
    "ctl00$pageContent$courseLevelDropDown":"",
    "ctl00$pageContent$startTimeFromDropDown":"",
    "ctl00$pageContent$startTimeToDropDown":"",
    "ctl00$pageContent$daysCheckBoxList$0":"M",
    "ctl00$pageContent$daysCheckBoxList$1":"T",
    "ctl00$pageContent$daysCheckBoxList$2":"W",
    "ctl00$pageContent$daysCheckBoxList$3":"R",
    "ctl00$pageContent$daysCheckBoxList$4":"F",
    "ctl00$pageContent$daysCheckBoxList$5":"S",
    "ctl00$pageContent$daysCheckBoxList$6":"U",
    "ctl00$pageContent$unitsFromDropDown":"0",
    "ctl00$pageContent$unitsToDropDown":"12",
    "ctl00$pageContent$enrollcodeTextBox":"",
    "ctl00$pageContent$instructorTextBox":"",
    "ctl00$pageContent$keywordTextBox":"",
    "ctl00$pageContent$GECollegeDropDown":"",
    "ctl00$pageContent$GECodeDropDown":"",
    "ctl00$pageContent$searchButton":"Begin+Search",
}
login_url = "https://my.sa.ucsb.edu/gold/Login.aspx"
find_url = "https://my.sa.ucsb.edu/gold/CriteriaFindCourses.aspx"
scrape_url = "https://my.sa.ucsb.edu/gold/ResultsFindCourses.aspx"
home_url = "https://my.sa.ucsb.edu/gold/Home.aspx"
session = requests.session()
session.post(url=login_url, data=login)
for category in categories:
     find["ctl00$pageContent$departmentDropDown"] = category
     session.post(url=find_url, data=find)
     url = session.get(url=scrape_url)
open("scrape.html", "w").write(url.content.decode("utf-8"))
