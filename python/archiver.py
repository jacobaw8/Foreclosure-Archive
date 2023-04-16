# ============================================================================== #
#                                    IMPORTS                                     #

import requests
import re
from bs4 import BeautifulSoup
import time
import random
import os
from datetime import datetime
import csv
import PyPDF2
import mysql.connector

from seleniumwire import webdriver

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire.utils import decode
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#                                   END IMPORTS                                  #
# ============================================================================== #







# ============================================================================== #
#                             GLOBAL VARIABLES                                   #

WEIRD_CODE_THING = "lcf12yrczmbw1kgmb5b4axi1"

#removed API_KEY for github entry
API_KEY = ""
LIST_URL = "https://www.ncnotices.com/(S(" + WEIRD_CODE_THING + "))/Search.aspx"
MAIN_URL = "https://www.ncnotices.com/(S(" + WEIRD_CODE_THING + "))/"

LISTINGS_CHECKED = 0
LISTINGS_GATHERED = 0
LISTINGS_FAILED = 0

#                           END GLOBAL VARIABLES                                 #
# ============================================================================== #








# ============================================================================== #
#                                   FUNCTIONS                                    #

def getPDFData(link):
    r = requests.get(link)
    if r.status_code == 200:
        with open("current.pdf", "wb") as f:
            f.write(r.content)
    else:
        print("PDF Couldn't Open: " + r.status_code)

    pdfFileObj = open("current.pdf", 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
    #print(pdfReader.numPages)
    pageObj = pdfReader.getPage(0)
    text = pageObj.extractText()
    #print(text)
    pdfFileObj.close()
    os.remove("current.pdf")

    return text

def formatDate(date):
    
    month = re.findall("january|January|jan|Jan|february|February|feb|Feb|march|March|mar|Mar|april|April|apr|Apr|may|May|june|June|jun|Jun|july|July|jul|Jul|august|August|aug|Aug|september|September|sep|Sep|october|October|oct|Oct|november|November|nov|Nov|december|December|dec|Dec", date)
    month = month[0]
    month_numerical = "-1"
    if (month == 'january' or month == 'jan'):
        month_numerical = "01"
    elif (month == 'february' or month == 'feb'):
        month_numerical = "02"
    elif (month == 'march' or month == 'mar'):
        month_numerical = "03"
    elif (month == 'april' or month == 'apr'):
        month_numerical = "04"
    elif (month == 'may'):
        month_numerical = "05"
    elif (month == 'june' or month == 'jun'):
        month_numerical = "06"
    elif (month == 'july' or month == 'jul'):
        month_numerical = "07"
    elif (month == 'august' or month == 'aug'):
        month_numerical = "08"
    elif (month == 'september' or month == 'sep'):
        month_numerical = "09"
    elif (month == 'october' or month == 'oct'):
        month_numerical = "10"
    elif (month == 'november' or month == 'nov'):
        month_numerical = "11"
    elif (month == 'december' or month == 'dec'):
        month_numerical = "12"

    year = re.findall("\d{4}", date)
    year = year[0]
    year = year[-2:]

    day = re.findall(" \d?\d,? ", date)
    day = day[0]
    day = day.replace(",", "")
    day = day.replace(" ", "")

    formatted_date = str(month_numerical) + "/" + str(day) + "/" + str(year)

    return formatted_date

def grabDate(html):
    date = ""
    time = ""
    for res in re.findall("\d?\d a.m.", str(html).lower()):
        time = res
    for res in re.findall("\d?\d p.m.", str(html).lower()):
        time = res
    for res in re.findall("\d?\d am", str(html).lower()):
        time = res
    for res in re.findall("\d?\d pm", str(html).lower()):
        time = res

    for res in re.findall("\d?\d\d\d a.m.", str(html).lower()):
        time = res
    for res in re.findall("\d?\d\d\d p.m.", str(html).lower()):
        time = res
    for res in re.findall("\d?\d\d\d am", str(html).lower()):
        time = res
    for res in re.findall("\d?\d\d\d apm", str(html).lower()):
        time = res

    for res in re.findall("\d?\d:\d\d a.m.", str(html).lower()):
        time = res
    for res in re.findall("\d?\d:\d\d p.m.", str(html).lower()):
        time = res
    for res in re.findall("\d?\d:\d\d pm", str(html).lower()):
        time = res
    for res in re.findall("\d?\d:\d\d am", str(html).lower()):
        time = res

    # if "pm" in time or "p.m." in time:
    #     time.replace("1:00", "13:00")
    #     time.replace("2:00", "14:00")
    #     time.replace("3:00", "15:00")
    #     time.replace("4:00", "16:00")
    #     time.replace("5:00", "17:00")
    #     time.replace("6:00", "18:00")
    #     time.replace("7:00", "19:00")
    #     time.replace("8:00", "20:00")
    #     time.replace("9:00", "21:00")
    #     time.replace("10:00", "22:00")
    #     time.replace("11:00", "23:00")
    #     time.replace("12:00", "24:00")
    time = time.replace("am", "AM")
    time = time.replace("a.m.", "AM")
    time = time.replace("pm", "PM")
    time = time.replace("p.m.", "PM")


    #print(str(html))

    # pattern 1
    for res in re.findall("t[ -]*h[ -]*e[ -]*u[ -]*n[ -]*d[ -]*e[ -]*r[ -]*s[ -]*i[ -]*g[ -]*n[ -]*e[ -]*d[ -]*s[ -]*u[ -]*b[ -]*s[ -]*t[ -]*i[ -]*t[ -]*u[ -]*t[ -]*e.+t[ -]*o[ -]*t[ -]*h[ -]*e[ -]*h[ -]*i[ -]*g[ -]*h[ -]*e[ -]*s[ -]*t[ -]*b[ -]*i[ -]*d[ -]*d[ -]*e[ -]*r[ -]*", str(html).lower()):
        for finalDate in re.findall("(?:january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec) [0-9]?[0-9],? ?[0-9]+", res.lower()):
            date = finalDate
            date = formatDate(date)
            if(time == ""):
                return datetime.strptime(date, "%m/%d/%y")
            fulldate = str(date) + " " + str(time)
            return datetime.strptime(fulldate, "%m/%d/%y %I:%M %p")
    
    # pattern 2
    for res in re.findall("t[ -]*h[ -]*e[ -]*u[ -]*n[ -]*d[ -]*e[ -]*r[ -]*s[ -]*i[ -]*g[ -]*n[ -]*e[ -]*d[ -]*t[ -]*r[ -]*u[ -]*s[ -]*t[ -]*e[ -]*e.*t[ -]*o[ -]*t[ -]*h[ -]*e[ -]*h[ -]*i[ -]*g[ -]*h[ -]*e[ -]*s[ -]*t[ -]*b[ -]*i[ -]*d[ -]*d[ -]*e[ -]*r[ -]*", str(html).lower()):
        for finalDate in re.findall("(?:january|January|jan|Jan|february|February|feb|Feb|march|March|mar|Mar|april|April|apr|Apr|may|May|june|June|jun|Jun|july|July|jul|Jul|august|August|aug|Aug|september|September|sep|Sep|october|October|oct|Oct|november|November|nov|Nov|december|December|dec|Dec) [0-9]?[0-9],? ?[0-9]+", res.lower()):
            date = finalDate
            date = formatDate(date)
            if(time == ""):
                return datetime.strptime(date, "%m/%d/%y")
            fulldate = str(date) + " " + str(time)
            return datetime.strptime(fulldate, "%m/%d/%y %I:%M %p")

    # pattern 3
    for res in re.findall("d[ -]*a[ -]*t[ -]*e[ -]*o[ -]*f[ -]*s[ -]*a[ -]*l[ -]*e[ -]*:[ -]*(?:january|January|jan|Jan|february|February|feb|Feb|march|March|mar|Mar|april|April|apr|Apr|may|May|june|June|jun|Jun|july|July|jul|Jul|august|August|aug|Aug|september|September|sep|Sep|october|October|oct|Oct|november|November|nov|Nov|december|December|dec|Dec) [0-9]?[0-9],? ?[0-9]+", str(html).lower()):
        date = res.replace("date of sale: ", "")
        date = formatDate(date)
        if(time == ""):
            return datetime.strptime(date, "%m/%d/%y")
        fulldate = str(date) + " " + str(time)
        return datetime.strptime(fulldate, "%m/%d/%y %I:%M %p")

    # pattern 4
    for res in re.findall("a[ -]*t[ -]*t[ -]*h[ -]*e[ -]*c[ -]*o[ -]*u[ -]*r[ -]*t[ -]*h[ -]*o[ -]*u[ -]*s[ -]*e[ ]*d[ -]*o[ -]*o[ -]*r.*\.m\.", str(html).lower()):
        for finalDate in re.findall("(?:january|January|jan|Jan|february|February|feb|Feb|march|March|mar|Mar|april|April|apr|Apr|may|May|june|June|jun|Jun|july|July|jul|Jul|august|August|aug|Aug|september|September|sep|Sep|october|October|oct|Oct|november|November|nov|Nov|december|December|dec|Dec) [0-9]?[0-9],? ?[0-9]+", res.lower()):
            date = finalDate
            date = formatDate(date)
            if(time == ""):
                return datetime.strptime(date, "%m/%d/%y")
            fulldate = str(date) + " " + str(time)
            return datetime.strptime(fulldate, "%m/%d/%y %I:%M %p")

    # pattern 5
    # 9th day of December, 2022,
    for res in re.findall("a[ -]*t[- ]+t[ -]*h[ -]*e[- ]*c[ -]*o[ -]*u[ -]*r[ -]*t[ -]*h[ -]*o[ -]*u[ -]*s[ -]*e[- ]*d[ -]*o[ -]*o[ -]*r.*[0-9]{4}", str(html).lower()):
        for finalDate in re.findall("[0-9]?[0-9](?:th|st|rd) day of (?:january|January|jan|Jan|february|February|feb|Feb|march|March|mar|Mar|april|April|apr|Apr|may|May|june|June|jun|Jun|july|July|jul|Jul|august|August|aug|Aug|september|September|sep|Sep|october|October|oct|Oct|november|November|nov|Nov|december|December|dec|Dec),? ?[0-9]+", res.lower()):
            date = finalDate
            date = formatDate(date)
            if(time == ""):
                return datetime.strptime(date, "%m/%d/%y")
            fulldate = str(date) + " " + str(time)
            return datetime.strptime(fulldate, "%m/%d/%y %I:%M %p")

    # pattern 6
    # 9th day of December, 2022,
    for res in re.findall("s[ -]*a[ -]*l[ -]*e[ -]*w[ -]*i[ -]*l[ -]*l[ -]*b[ -]*e[ -]*h[ -]*e[ -]*l[ -]*d.+c[ -]*o[ -]*u[ -]*r[ -]*t[ -]*h[ -]*o[ -]*u[ -]*s[ -]*e.+\.m\.", str(html).lower()):
        for finalDate in re.findall("(?:january|January|jan|Jan|february|February|feb|Feb|march|March|mar|Mar|april|April|apr|Apr|may|May|june|June|jun|Jun|july|July|jul|Jul|august|August|aug|Aug|september|September|sep|Sep|october|October|oct|Oct|november|November|nov|Nov|december|December|dec|Dec) [0-9]?[0-9],? ?[0-9]+", res.lower()):
            date = finalDate
            date = formatDate(date)
            if(time == ""):
                return datetime.strptime(date, "%m/%d/%y")
            fulldate = str(date) + " " + str(time)
            return datetime.strptime(fulldate, "%m/%d/%y %I:%M %p")
            
    # error: couldn't locate pattern
    f = open("nodate", "w+")
    f.write(str(html).lower())
    f.close()
    return "Couldn't locate date of sale"


def grabCaseNum(html):
    spNum = ""
    for res in re.findall("[0-9]+ sp [0-9]+", str(html).lower()):
        spNum = res
        return spNum
    cvsNum = ""
    for res in re.findall("[0-9]+ cvs [0-9]+", str(html).lower()):
        cvsNum = res
        return cvsNum
    cvdNum = ""
    for res in re.findall("[0-9]+ cvd [0-9]+", str(html).lower()):
        cvdNum = res
        return cvdNum

    # unformatted_curr_date = str(datetime.now())
    # unformatted_curr_date = unformatted_curr_date.replace(".", " ")
    # unformatted_curr_date = unformatted_curr_date.replace(":", " ")
    # formatted_curr_date = unformatted_curr_date.replace("-", "-")

    # f = open("SP NOT FOUND " + formatted_curr_date + ".txt", "w+")
    # f.write(str(html))
    # f.close()

    return "Case number not found"

# Too hard to find the attorney and bank for the time being... Try to find it later at some point.... #
# 
# def grabAttorney(html):
#     attorney = ""
#     for res in re.findall(".{2} undersigned .{100}", str(html).lower()):
#         print(res)
#         return

# def grabBank(html):
#     return





def grabCounty(html):
    county = ""
    for res in re.findall(" [a-zA-Z]+ county ", str(html).lower()):
        county = res
        print(res)
        return county
    for res in re.findall(" county of [a-zA-Z]+ ", str(html).lower()):
        county = res
        print(res)
        return county
    for res in re.findall(" of the county [a-zA-Z]+ ", str(html).lower()):
        county = res
        print(res)
        return county
    return county

def grabAddress(html):
    address = ""
    # for res in re.findall("(\\d{1,}) [a-zA-Z0-9\\s]+(\\,)? [a-zA-Z]+(\\,)? [A-Z]{2} [0-9]{5,6}", str(html)):
    #     print(res)
    #     return

    flag = 0
    result = ""
    res = ""

    for res in re.findall("address of property: .+ \d{5}", str(html).lower()):
        print("1")
        result = res
        flag = 1
    for res in re.findall("address of property: .+ nc", str(html).lower()):
        print("2")
        if flag == 0:
            flag = 1
            result = res
    for res in re.findall("address of property: .+ north carolina", str(html).lower()):
        print("3")
        result = res
        if flag == 0:
            flag = 1
            result = res

    for res in re.findall("property address: \d{5}", str(html).lower()):
        print("4")
        result = res
        if flag == 0:
            flag = 1
            result = res
    for res in re.findall("property address: nc", str(html).lower()):
        print("5")
        result = res
        if flag == 0:
            flag = 1
            result = res
    for res in re.findall("property address: north carolina", str(html).lower()):
        print("6")
        if flag == 0:
            flag = 1
            result = res

    for res in re.findall("address.+ \d{5}", str(html).lower()):
        print("7")
        if flag == 0:
            flag = 1
            result = res
    for res in re.findall("address.+ nc", str(html).lower()):
        print("8")
        if flag == 0:
            flag = 1
            result = res
    for res in re.findall("address.+ north carolina", str(html).lower()):
        print("9")
        if flag == 0:
            flag = 1
            result = res

    for res in re.findall("property located at.+ \d{5}", str(html).lower()):
        print("10")
        if flag == 0:
            flag = 1
            result = res
    for res in re.findall("property located at.+ nc", str(html).lower()):
        print("11")
        if flag == 0:
            flag = 1
            result = res
    for res in re.findall("property located at.+ north carolina", str(html).lower()):
        print("12")
        if flag == 0:
            flag = 1
            result = res

    for res in re.findall("property being located at.+ \d{5}", str(html).lower()):
        print("13")
        if flag == 0:
            flag = 1
            result = res
    for res in re.findall("property being located at.+ nc", str(html).lower()):
        print("14")
        if flag == 0:
            flag = 1
            result = res
    for res in re.findall("property being located at.+ north carolina", str(html).lower()):
        print("15")
        if flag == 0:
            flag = 1
            result = res

    for res in re.findall("commonly known as.+ \d{5}", str(html).lower()):
        print("16")
        if flag == 0:
            flag = 1
            result = res
    for res in re.findall("commonly known as .+ nc", str(html).lower()):
        print("17")
        if flag == 0:
            flag = 1
            result = res
    for res in re.findall("commonly known as .+ north carolina", str(html).lower()):
        print("18")
        if flag == 0:
            flag = 1
            result = res

    for res in re.findall("lying and being known as.+ \d{5}", str(html).lower()):
        print("19")
        if flag == 0:
            flag = 1
            result = res
    for res in re.findall("lying and being known as.+ nc", str(html).lower()):
        print("20")
        if flag == 0:
            flag = 1
            result = res
    for res in re.findall("lying and being known as.+ north carolina", str(html).lower()):
        print("21")
        if flag == 0:
            flag = 1
            result = res

            

    count = 0
    printed = 0
    newstring = ""
    for letter in res:
        newstring += letter
        if letter.isdigit():
            count += 1
            if(count == 5):
                if printed == 0:
                    print(newstring)
                    return newstring
                    printed = 1
        else:
            count = 0

    if printed == 0:
        split_text = res.split("north carolina", 1)
        if(len(split_text) > 1):
            printed = 1
            
            print(split_text[0] + "north carolina")
            return split_text[0] + "north carolina"

    if printed == 0:
        split_text = res.split("nc", 1)
        if(len(split_text) > 1):
            printed = 1
            print(split_text[0] + "nc")
            return split_text[0] + "nc"

    return res

# def grabDefendent(html):
#     defendent = ""
#     for res in re.findall("", str(html)):
#         print(res)
#     return

def grabPhoneNumber(html):
    phone = ""
    for res in re.findall("\d{3}-\d{3}-\d{4}", str(html)):
        print(res)
        phone = res
    return phone

def grabTrailerIfExists(html):
    if " vin " in str(html).lower():
        return True
    return False

def parseData(html, link, id):
    flag = 0
    for pdf in re.findall("PDFDocument.aspx.+id=", str(html)):
        pdf = pdf.replace("\" id=", "")
        pdf = pdf.replace("amp;", "")
        url = MAIN_URL + str(pdf)
        html = getPDFData(url)
        parseData(html, url, id)

        flag = 1

    if flag == 0:
        date = grabDate(html)
        caseNum = grabCaseNum(html)

        print("Date: " + str(date))
        print("Case Number: " + caseNum)
        print("County: ")
        county = grabCounty(html)
        print("Address: ")
        address = grabAddress(html)
        print("Phone Number: ")
        phone = grabPhoneNumber(html)
        isTrailer = grabTrailerIfExists(html)
        isTrailerText = ""
        if isTrailer:
            isTrailerText = "Trailer"
        else:
            isTrailerText = "No Trailer"
        
        write = 0
        with open('archiver.csv', encoding='windows-1252') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                temp_row = ",".join(row)
                if str(date) in temp_row and caseNum.replace(",", "") in temp_row and county.replace(",", "") in temp_row and address.replace(",", "") in temp_row and phone.replace(",", "") in temp_row:
                    write = 1

            csv_file.close()
        if(write == 0):
            print("UNIQUE")
            f = open("archiver.csv", "a")
            f.write("\n" + str(date) + "," + caseNum.replace(",", "") + "," + county.replace(",", "") + "," + address.replace(",", "") + "," + phone.replace(",", "") + "," + isTrailerText.replace(",", "") + "," + link + " ," + id)
            f.close()
        else:
            print("\nALREADY HERE\n")
        #grabAttorney(html)
        #print(date)
    print("\n\n")
    return




def captcha(INDIVIDUAL_URL, html, id_thing):
    print("===============================================================\n                         CAPTCHA ALERT\n===============================================================")
    grab = requests.get(INDIVIDUAL_URL)
    soup = BeautifulSoup(grab.content, 'html.parser')
    site_key = soup.find("div", {"class" : "recaptcha"})
    site_key_final = site_key['data-sitekey']


    form = {"method": "userrecaptcha",
            "googlekey": site_key_final,
            "key": API_KEY,
            "pageurl": INDIVIDUAL_URL,
            "json": 1}

    response = requests.post('http://2captcha.com/in.php', data=form)
    print(response.json())
    request_id = response.json()['request']
    url = f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={request_id}&json=1"
        
    driver = webdriver.Chrome(executable_path=chromepath, options=options, desired_capabilities=capabilities)
    driver.get(INDIVIDUAL_URL)

    status = 0
    while not status:
        res = requests.get(url)
        if res.json()['status']==0:
            time.sleep(3)
        else:
            requ = res.json()['request']
            time.sleep(5)
            js = f'document.getElementById("g-recaptcha-response").innerHTML="{requ}";'
            print(requ)
            driver.execute_script(js)
            driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_btnViewNotice").click()
            driver.quit()
            time.sleep(2)
            f = open("html.txt", "w")
            f.write(str(html))
            f.close()
            burp0_url = INDIVIDUAL_URL
            burp0_cookies = {"__utma": "227932034.1343111823.1670096268.1670096268.1670096268.1", "__utmb": "227932034", "__utmc": "227932034", "__utmz": "227932034.1670096268.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none)", "_ga_D6RWGVZGWW": "GS1.1.1670096269.1.1.1670097961.54.0.0", "_ga": "GA1.2.530345704.1670096270", "_gid": "GA1.2.917216944.1670096270", "_gat_gtag_UA_42595872_24": "1", ".ASPXAUTH": "C4E7A6374AD2E05EB94097C9438AEFFEEA21B6BF6639F1174F58F46F53B50559B575A6DE41E07043BF59BACA3C90DDA0B29E54042777AC89E1F46100244768E7929D807B69F880A82DC31EEB37D37CDB54802781BA986B30BE8AF14771F9545DC081A1F44C102FC44EE23AC25A53A2410DB8A3D1C0D84FFBDC8F592E029D3140CED881C13D2C59FB5334E13418819C72C364BA5D"}
            burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://www.ncnotices.com/(S(nai5plhhkuezyzpppl0gu0t5))/Authenticate.aspx?ReturnUrl=%2fSearch.aspx", "Upgrade-Insecure-Requests": "1", "Te": "trailers"}
            res = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
            html = BeautifulSoup(res.content,'html.parser')
            parseData(html, burp0_url, id_thing)
            print("success")
            status = 1

    return

#                                 END FUNCTIONS                                  #
# ============================================================================== #



chromepath = "/var/www/html/python/chromedriver"
options = webdriver.ChromeOptions()
options.binary_location = r'/var/www/html/chromedriver'
#options.add_argument("user-data-dir=C:\\Users\\Jacob\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
options.add_argument("--ignore-certificate-errors")
options.add_argument("headless")

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}



burp0_url = LIST_URL
burp0_cookies = {"__utma": "227932034.1343111823.1670096268.1670096268.1670096268.1", "__utmb": "227932034", "__utmc": "227932034", "__utmz": "227932034.1670096268.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none)", "_ga_D6RWGVZGWW": "GS1.1.1670096269.1.1.1670097961.54.0.0", "_ga": "GA1.2.530345704.1670096270", "_gid": "GA1.2.917216944.1670096270", "_gat_gtag_UA_42595872_24": "1", ".ASPXAUTH": "C4E7A6374AD2E05EB94097C9438AEFFEEA21B6BF6639F1174F58F46F53B50559B575A6DE41E07043BF59BACA3C90DDA0B29E54042777AC89E1F46100244768E7929D807B69F880A82DC31EEB37D37CDB54802781BA986B30BE8AF14771F9545DC081A1F44C102FC44EE23AC25A53A2410DB8A3D1C0D84FFBDC8F592E029D3140CED881C13D2C59FB5334E13418819C72C364BA5D"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://www.ncnotices.com/(S(nai5plhhkuezyzpppl0gu0t5))/Authenticate.aspx?ReturnUrl=%2fSearch.aspx", "Upgrade-Insecure-Requests": "1", "Te": "trailers"}
res = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)


# ============================================================================== #
#                 find all ID's in response.... Format should be:                #
#                                   ID=______&#                                  #
# ============================================================================== #

html = BeautifulSoup(res.content,'html.parser')

for id in re.findall("ID=[0-9]{6}", str(html)):

    time.sleep(random.uniform(4.25, 8.5))
    print(id.replace("ID=", ""))
    final_id = id.replace("ID=", "")

    flag = 0
    with open('archiver.csv', encoding='windows-1252') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                temp_row = ",".join(row)
                if final_id in temp_row:
                    flag = 1
    if (flag == 1):
        print("Already captured this listing.")
        continue

    WEIRD_ID_THING = final_id
    INDIVIDUAL_URL = "https://www.ncnotices.com/(S(" + WEIRD_CODE_THING + "))/Details.aspx?SID=" + WEIRD_CODE_THING + "&ID=" + WEIRD_ID_THING


    burp0_url = INDIVIDUAL_URL
    burp0_cookies = {"__utma": "227932034.1343111823.1670096268.1670096268.1670096268.1", "__utmb": "227932034", "__utmc": "227932034", "__utmz": "227932034.1670096268.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none)", "_ga_D6RWGVZGWW": "GS1.1.1670096269.1.1.1670097961.54.0.0", "_ga": "GA1.2.530345704.1670096270", "_gid": "GA1.2.917216944.1670096270", "_gat_gtag_UA_42595872_24": "1", ".ASPXAUTH": "C4E7A6374AD2E05EB94097C9438AEFFEEA21B6BF6639F1174F58F46F53B50559B575A6DE41E07043BF59BACA3C90DDA0B29E54042777AC89E1F46100244768E7929D807B69F880A82DC31EEB37D37CDB54802781BA986B30BE8AF14771F9545DC081A1F44C102FC44EE23AC25A53A2410DB8A3D1C0D84FFBDC8F592E029D3140CED881C13D2C59FB5334E13418819C72C364BA5D"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://www.ncnotices.com/(S(nai5plhhkuezyzpppl0gu0t5))/Authenticate.aspx?ReturnUrl=%2fSearch.aspx", "Upgrade-Insecure-Requests": "1", "Te": "trailers"}
    res = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
    html = BeautifulSoup(res.content,'html.parser')
    if("Notice Content" in str(html)):

        parseData(html, INDIVIDUAL_URL, final_id)

    else:

        captcha(INDIVIDUAL_URL, html, final_id)
        
        

        #grab site key
        #query 2captcha
        #wait for response
        #post response

        #print(html)
        

#f = open("output.txt", "w")
#f.write(str(res.content))
#print(res.content)