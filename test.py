#importing essentials
from flask import Flask, render_template
import requests
from flask import request
import json
import datetime
from datetime import datetime,timedelta

app = Flask(__name__)

# displays the html form
@app.route("/")
def form():
    return render_template('form_submit.html')

# receiving the url from html form

@app.route('/hello/', methods=['POST'])
def hello():
    if request.method == 'POST':
        url = request.form['url']

# spliting the url to create create a customize url for visiting the git api
        path = url.split("/")[1:]
        print path
        url = 'https://api.github.com/'+'repos'+'/'+path[2]+'/'+path[3]


### trying to fetch No of open issues in 24 hours,24 hrs and but less than 7 days and older than 7 days.

#current time - 24hrs and formating according to ISO 8601
    now = (datetime.now() - timedelta(minutes=1440))
    time_24hrs_back = now.isoformat()
    time_24hrs_back = time_24hrs_back.replace('.','Z+')
    time_24hrs_back = time_24hrs_back.split("+")

    #current time - 7days
    now7 = (datetime.now() - timedelta(days=7))
    mintwo = (now - now7)
    seconds = mintwo.total_seconds()
    ###
    days = seconds % 84000
    hours = 00
    minutes = 00

    ###
    mintwo = str(now.year)+'-'+str(now.month)+'-'+str(mintwo.days)+'T'+str(hours)+':'+str(minutes)+':00Z'
    print mintwo
    now7 = now7.isoformat()
    now7 = now7.replace('.','Z+')
    now7 = now7.split("+")

    #Get the total number of open issues

    r = requests.get(url)
    if(r.ok):
        repoItem = json.loads(r.text or r.content)
        open_issues = repoItem['open_issues_count']

    # No of open issues in 24 hrs

    r = (url+'/issues?since='+time_24hrs_back[0])
    r = requests.get(r)
    if(r.ok):
        repo = json.loads(r.text or r.content)
        last_24_hours = len(repo)
        print last_24_hours



    # No of open issues < 7 days

    r = (url+'/issues?since='+str(mintwo))
    r = requests.get(r)
    if(r.ok):
        repo = json.loads(r.text or r.content)
        less_then_7days = len(repo)
        print less_then_7days


    # No of open issues more than 24hrs but less than 7days
        issues_last7 = less_then_7days - last_24_hours
        print str(issues_last7)


    #No of issues older than 7days
    issues_7days_ago = open_issues - less_then_7days






    ### render the html ###
    return render_template('form_action.html',url=url,issues_last7=issues_last7,last_24_hours=last_24_hours,open_issues=open_issues,issues_7days_ago=issues_7days_ago)


# Run the app :)
if __name__ == "__main__":
    app.debug = True
    app.run()
