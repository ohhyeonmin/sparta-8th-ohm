from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/order', methods=['POST'])
def write_order():
    name_receive = request.form['name_give']
    count_receive = request.form['count_give']
    add_receive = request.form['add_give']
    phone_receive = request.form['phone_give']

    # 클라이언트에서 받은 값을 MongoDB에 저장!
    db.houseorder.insert_one({
        'name': name_receive,
        'count': count_receive,
        'address': add_receive,
        'phone': phone_receive
    })

    # return jsonify({'result':'success', 'msg': '이 요청은 POST!'})
    return jsonify({'result':'success'})

@app.route('/order', methods=['GET'])
def read_order():
    orders = list(db.houseorder.find({}, {'_id': False}))
    # MongoDB에서 _id 제외한 모든 데이터 조회
    # Dictionary에 데이터 담기
    data = {
        'result': 'success',
        'orders': orders,
    }

    return jsonify(data)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)