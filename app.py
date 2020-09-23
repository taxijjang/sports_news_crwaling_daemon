from flask import Flask, request, jsonify
from redis import Redis
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def RedisCheck(flat_form, category):
    try:
        rconn = Redis(host='ec2-3-34-134-147.ap-northeast-2.compute.amazonaws.com', port=6379, db=1,
                      decode_responses=True)

        hset_key = flat_form + ':' + category
        data = rconn.hgetall(hset_key)
        # print(data)
        return data


    except Exception as e:
        print(str(e))


@app.route('/')
def index():
    return "Hello Flask"


@app.route('/info')
def info():
    return 'Info'


@app.route('/<flat_form>/<category>')
def news(flat_form, category):
    news_json = RedisCheck(flat_form=flat_form, category=category)

    print(news_json)
    return jsonify(news_json)


if __name__ == "__main__":
    app.run()

RedisCheck()
