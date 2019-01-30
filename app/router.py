import sqlite3
from flask import Flask,request
from flask_cors import CORS
import json
from app import app

# 创建数据库,存储图片
@app.route('/set',methods=['GET','POST'])
def get_info():
    conn = sqlite3.connect('SQLLITE.db')
    cursor = conn.cursor()
    data = request.get_data()
    if not data:
        return json.dumps({
        "code":404
    })
    json_re = json.loads(data.decode('utf-8'))

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

    cursor.execute('CREATE TABLE IF NOT EXISTS user(time, url,img_id)')
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

# 根据时间取出数据
@app.route('/date',methods=['GET','POST'])
def get_time_img():
    conn = sqlite3.connect('SQLLITE.db')
    cursor = conn.cursor()
    data = request.get_data()

    json_re = json.loads(data.decode('utf-8'))
    print(json_re['beginTime'])
    beginTime = json_re['beginTime']
    endTime = json_re['endTime']

    cursor.execute('SELECT * FROM user WHERE time > \'%d\' AND time < \'%d\'' % (beginTime,endTime))

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
    json_re = json.loads(data.decode('utf-8'))
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

#text数据存储
@app.route('/edit',methods=['GET','POST'])
def edit_text():

    conn = sqlite3.connect('SQLLITE.db')
    cursor = conn.cursor()

    data=request.get_data()
    json_re = json.loads(data.decode('utf-8'))
    print(json_re)
    title = json_re['title']
    content = json_re['content']
    print(title,content)
    cursor.execute('CREATE TABLE IF NOT EXISTS text_table(id INTEGER PRIMARY KEY AUTOINCREMENT,title, content)')
    cursor.execute("INSERT INTO text_table(title, content) VALUES (\'%s\',\'%s\')" % (title, content))
    cursor.close()
    conn.commit()
    conn.close()

    return json.dumps({
        "code":0
    })


# 获取text 数据
@app.route('/text',methods=['GET','POST'])
def text_all():

    data=request.get_data()
    json_re = json.loads(data.decode('utf-8'))

    print(json_re)

    conn = sqlite3.connect('SQLLITE.db')
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS text_table(id INTEGER PRIMARY KEY AUTOINCREMENT,title, content)')

    sql=''
    if json_re['type']=='title':
        sql = 'SELECT id,title FROM text_table'
    if json_re['type']=='detail':
        detail_id = json_re['id']
        sql = 'SELECT * FROM text_table WHERE id = \'%s\''%(detail_id)
    if json_re['type'] == 'delete':
        detail_id = json_re['id']
        sql = 'DELETE FROM text_table WHERE id = \'%s\'' % (detail_id)

    cursor.execute(sql)
    sql_data = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()


    list_sql = []
    if len(sql_data) > 0:
        for i in range(len(sql_data)):
            if json_re['type'] == 'title':
              list_sql.append({"id": sql_data[i][0],"title":sql_data[i][1]})
            if json_re['type'] == 'detail':
                list_sql.append({"id": sql_data[i][0], "title": sql_data[i][1],"content":sql_data[i][2]})

    return json.dumps({
        "code":0,
        "data":list_sql
    })