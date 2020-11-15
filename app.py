from flask import Flask, jsonify
from redis import Redis
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

rconn = Redis(host='ec2-3-34-134-147.ap-northeast-2.compute.amazonaws.com', port=6379, db=1,
              decode_responses=True)
@app.route('/')
def base_url():
    response = dict(code=200, status="OK", message=[])
    return jsonify(response)

@app.route('/flat_form_list')
def flat_form_list():
    response = dict(code=200, status="OK", message=[])
    key = 'flat_form_list'
    data = list(rconn.smembers(key))
    response['message'] = data
    return jsonify(response)


@app.route('/flat_form_list/<flat_form>')
def category_list(flat_form):
    response = dict(code=200, status="OK", message=[])

    category_lists = list()
    flat_form_key = flat_form + ':*'
    for key in rconn.keys(flat_form_key):
        _, category = key.split(':')
        category_lists.append(category)

    response['message'] = category_lists

    return jsonify(response)


@app.route('/<flat_form>/<category>')
def news(flat_form, category):
    response = dict(code=200, status="OK", message=[])
    key = flat_form + ':' + category
    try:
        data = rconn.get(key)
        news_json = json.loads(data)

        response['message'] = news_json
        return jsonify(response)
    except Exception as e:
        print(e)
        response['code'] = 400
        response['status'] = 'NOT_VALID_DATA'
        return response


if __name__ == "__main__":
    app.debug = True
    app.run()
