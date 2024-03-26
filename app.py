from flask import Flask
from flask import render_template
import sqlite3

# from sqlalchemy import create_engine, Metadata, Table, Column, String
# from sqlalchemy.orm import sessionmaker
# from flask_paginate import Paginate

app = Flask(__name__)


@app.route('/index')
@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/movie')
def movie():
    datalist = []
    con = sqlite3.connect('movie250.db')
    cur = con.cursor()
    sql = "SELECT * FROM movie250"
    data = cur.execute(sql)
    for row in data:
        datalist.append(row)
    cur.close()
    con.close()
    return render_template('movie.html', movies=datalist)


@app.route('/score')
def score():
    score = []  # 评分
    num = []  # 每一个电影评分对应的电影数量
    con = sqlite3.connect('movie250.db')
    cur = con.cursor()
    sql = 'SELECT score, COUNT(score) FROM movie250 GROUP BY score'
    data = cur.execute(sql)
    for row in data:
        score.append(str(row[0]))
        num.append(row[1])
    cur.close()
    con.close()
    return render_template('score.html', score=score, num=num)


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/word')
def word():
    return render_template('word.html')


if __name__ == '__main__':
    app.run()
