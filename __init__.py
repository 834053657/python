#!python
#coding:utf-8

import sqlite3
from flask import Flask,request
from flask_cors import CORS
import json

app = Flask(__name__)
# 跨域
CORS(app, resources=r'/*')


# 创建数据库,存储图片
@app.route('/set',methods=['GET','POST'])
def get_info():
    conn = sqlite3.connect('SQLLITE.db')
    cursor = conn.cursor()
    data = request.get_data()
    json_re = json.loads(data)

    for i in range(len(json_re)):
        time_v = json_re[i]['time']
        url_v = json_re[i]['url']
        img_id_v = json_re[i]['img_id']
        # cursor.execute('ALTER TABLE user ADD COLUMN img_id')
        cursor.execute('CREATE TABLE IF NOT EXISTS user(time, url,img_id)')
        cursor.execute("INSERT INTO user (time,url,img_id) VALUES (\'%s\',\'%s\',\'%s\')" % (time_v, url_v,img_id_v))
    cursor.close()
    conn.commit()
    conn.close()
    return json.dumps({
        "code":0
    })


# 取出数据
@app.route('/img',methods=['GET','POST'])
def post_img():
    conn = sqlite3.connect('SQLLITE.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user')

    sql_data = cursor.fetchall()
    list_sql = []
    if len(sql_data) > 0:
        for i in range(len(sql_data)):
            list_sql.append({'timer': sql_data[i][0], 'url': sql_data[i][1], 'img_id':sql_data[i][2]})
    cursor.close()
    conn.commit()
    conn.close()

    return json.dumps({
        "code":0,
        "data":list_sql
    })


#删除数据
@app.route('/delete',methods=['GET','POST'])
def delete_img():
    data = request.get_data()
    json_re = json.loads(data)
    print(json_re['img_id'])
    id = json_re['img_id']

    conn = sqlite3.connect('SQLLITE.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user WHERE img_id = (\'%s\')' % (id))
    cursor.close()
    conn.commit()
    conn.close()

    return json.dumps({
        "code":0
    })


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8001)

