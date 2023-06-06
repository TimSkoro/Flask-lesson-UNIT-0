import time

from flask import Flask, render_template, request
import requests
import json
from redis import Redis

from utils import get_news_with_params

# request == http packet

app = Flask(__name__)
db = Redis('127.0.0.1', 6380)

meta_data = {
    "last_id": 2
}
# news = [
#     {
#         "id": 1,
#         "title": "Breaking News!",
#         "description": "V belarisi shou slushok chto Luka nash petushok!",
#         "bad_news": 0
#     },
#     {
#         "id": 2,
#         "title": "Preparing invation on Belarus!",
#         "description": "4 position! I had got a map!",
#         "bad_news": 1
#     },
# ]


@app.route('/news', methods=["POST", "GET"])
def news_page():
    news = json.loads(db.get('news') or "[]")
    last_id = json.loads(db.get('last_id'))

    if request.method == 'POST':
        new_news = dict(request.form)
        new_news['id'] = last_id + 1
        new_news['bad_news'] = int(new_news['bad_news'])
        news.append(new_news)
        db.set('news', json.dumps(news))
        db.set('last_id', last_id + 1)

    parameters = request.args.to_dict()
    data = get_news_with_params(news, parameters)
    return render_template('news_page.html', data=data)


@app.route('/news/<int:news_id>', methods=['POST'])
def delete_news(news_id):
    news_index = news.index(list(filter(lambda n: n.get('id', 0) == news_id, news))[0])
    news.pop(news_index)
    return render_template('news_page.html', data=news)


@app.route('/api/news', methods=["POST", "GET"])
def news_view():
    if request.method == "POST":
        new_news = json.loads(request.data.decode('utf-8'))
        meta_data['last_id'] += 1
        new_news['id'] = meta_data['last_id']
        news.append(new_news)
    return news


@app.route('/post', methods=["POST", "GET"])
def post_test():
    if request.method == "POST":
        return "You made POST query"
    return "You made GET query"


@app.route('/')  # GET
def hello_world():  # put application's code here
    return render_template('home_page.html')


@app.route('/ok')
def ok():  # put application's code here
    return "You made your choice: 'Yes'"


@app.route('/first')
def first():
    # template = "<h1>Current time: {}</h1>"
    # return template.format(time.ctime())
    # return render_template('first_page.html', context={'my_time': time.ctime()})
    # bitcoin_price = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd').json()['bitcoin']['usd']
    return render_template('first_page.html', my_time=time.ctime(), btprice=0)


@app.route('/vote')
def vote():  # put application's code here
    return render_template('vote_page.html')


@app.route('/putin')
def trust():  # put application's code here
    return '<h1>HUILO</h1>'


@app.route('/time')
def current_time():
    return {
        'time': time.ctime(),
        'unixtime': time.time(),
        'timezone': 0,
    }


@app.route('/dinpar/<par1>/<int:par2>')
def dinpar(par1, par2):
    return {
        'data': (par1, par2),
        'type': (str(type(par1)), str(type(par2))),
        'result': par1 * par2
    }


if __name__ == '__main__':
    app.run()
