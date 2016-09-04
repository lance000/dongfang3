__author__ = 'root'
#!/usr/bin/env python


import requests
import json
import smtplib
import time
import datetime


def print_string_in_json_format(json_string):
    """
    This function will print the json non formatted string to json formatted string
    """
    parsed = json.loads(json_string)
    pretty_json_format = json.dumps(parsed, indent=4)
    return pretty_json_format

def json_format_to_dict(string):
    """
    This function will print the json formatted to dict
    """
    parsed = json.dumps(string)
    pretty_dict = json.loads(parsed)
    return pretty_dict

date = datetime.datetime.now()
date_month = datetime.datetime.now().strftime("%m")

month_table = {'01':31,'02':28,'03':31,'04':30,'05':31,'06':30, '07':31,'08':31,'09':30,'10':31,'11':30,'00':31}


date_list = []
i = 0

while i < 3:
    date_list.append(date.strftime("%Y-%m-%d"))
    date1_month = (int(date_month) + i)%12
    date11_month = "%02d" % date1_month
    time_delta = month_table[date11_month]
    date = date + datetime.timedelta(days = time_delta)
    i = i + 1

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

lowest_cost = {}

#print(date_list)

for date_url in date_list:
    url1 = "http://www.ceair.com/booking/new-low-price-calendar!getDynDayLowPriceEc.shtml?cond.monthOffSet=0&cond.depCode=PVG&cond.arrCode=HET&cond.trip=OW&cond.goDt=&cond.depDate=" + date_url + "&cond.currency=CNY"
    #print(url1)
    response = requests.get(url1, headers = headers)
    page = json.loads(response.content.decode('utf-8'))
    data1 = list(page['currentList'])
    for k in data1:
        #print(k)
        if 'lowest' in k:
            #print(k['d'] + " cost is " + k['p'])
            lowest_cost[k['d']] = k['p']


lowest= sorted(lowest_cost.items(), key=lambda d:d[1], reverse = False)
message = []
#print(lowest)

if float(lowest[0][1]) <= 460:
    for kk in lowest:
        if float(kk[1]) == float(lowest[0][1]):
            message.append(kk[0])
    message1 = (',').join(message)
    cost1 = lowest[0][1]
    print(cost1)

    text = 'From: zhiyqiu@cisco.com\nTo: 13564264302@139.com\nSubject:'+ cost1 + message1 +'\r\nText: Dongfang\n\n'
    username = '13564264302@139.com'
    password = 'q8446605'
    smtp = smtplib.SMTP()
    smtp.connect('smtp.139.com')
    smtp.login(username, password)
    smtp.sendmail('13564264302@139.com', '13564264302@139.com', text)

else:
    print("the lowest ticket cost %s is too expensive" % lowest[0][1])



