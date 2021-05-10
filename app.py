import requests
from flask import Flask
from flask import render_template
from datetime import date, timedelta, datetime

app = Flask(__name__)

BASE_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=389&date="

def days_cur_month():
    m = datetime.now().month
    y = datetime.now().year
    ndays = (date(y, m+1, 1) - date(y, m, 1)).days
    d1 = date(y, m, 1)
    d2 = date(y, m, ndays)
    delta = d2 - d1

    return [(d1 + timedelta(days=i)).strftime('%d-%m-%Y') for i in range(delta.days + 1)]

def get_availability(adate):
    centerFound = False

    URL = BASE_URL+ adate
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    states = requests.get(URL, headers=headers)
    centers = states.json()['centers']
    for center in centers:
        for validSession in center['sessions']:
            if validSession['min_age_limit'] == 18:
                if validSession['available_capacity'] > 0:
                    centerFound = True

    return centerFound, centers

@app.route('/')
@app.route('/getAvailability/<date>')
def getAvailability(date=None):
    if date != None:
        availability, centers = get_availability(date)
        return render_template('index.html', date=date, availability=availability, centers=centers)
    else:
        return render_template('index.html', date="", availability="", centers="")
