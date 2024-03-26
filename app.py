import sqlite3

from flask import Flask, request
from flask import render_template
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import create_engine, Table, Column, String, Integer, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:root123456@localhost:3306/douban250?charset=utf8mb4')
DBSession = sessionmaker(bind=engine)
metadata = MetaData()

m_movies = Table(
    'movie250', metadata,
    Column('id', Integer, primary_key=True),
    Column('info_link', String()),
    Column('pic_link', String()),
    Column('cname', String()),
    Column('ename', String()),
    Column('score', String()),
    Column('rated', String()),
    Column('introduction', String()),
    Column('info', String())
)

app = Flask(__name__)


@app.route('/index')
@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/movie')
def movie(page=None):
    # 定义当前页码，从第一页开始
    page = int(request.args.get('page', 1))
    # 定义每一页的数量
    per_page = 10
    sess = DBSession()
    movies = sess.query(m_movies).all()
    pagination = Pagination(page=page, per_page=per_page, total=len(movies))
    start = (page - 1) * per_page
    end = start + per_page
    movies = sess.query(m_movies).slice(start, end).all()
    print(movies)
    return render_template('movie.html', movies=movies, paginate=pagination)


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
