import requests
from flask import Flask, render_template, request,redirect
from bs4 import BeautifulSoup
from urllib.request import urlopen

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

app = Flask("DayEleven")

comments = []
selects = []

def crawl_data(input):
  response = requests.get(f'https://www.reddit.com/r/{input}/top/?t=month',headers=headers)
  soup = BeautifulSoup(response.text,'html.parser')
  boxes = soup.find_all("div",class_="_1oQyIsiPHYt6nx7VOmd1sz")
  selects.append(input)
  for box in boxes:
    content = box.find("h3",class_="_eYtD2XCVieq6emjKBH3m").get_text()
    upvote = box.find("div",class_="_1rZYMD_4xY3gRcSS3p8ODO").get_text()
    url = box.find("a",class_="_3jOxDPIQ0KaOWpzvSQo-1s").get_text()
    comment = {"input":input,"content":content,"upvote":upvote, "url":url}
    comments.append(comment)
  return comments


@app.route('/',methods=['POST','GET'])
def home():
  if request.method == 'GET':
    return render_template("home.html",subreddits=subreddits)
  elif request.method == 'POST':
    items = list(request.form.keys())
    for item in items:
      item = item.replace("/","")
      crawl_data(item)
    return redirect('/read')

@app.route('/read')
def read():
  return render_template("read.html",comments=comments,selects=selects)
  

app.run(host="0.0.0.0")