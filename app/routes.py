# -*- coding: utf-8 -*-

from flask import render_template
from app import app
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    dates = [
        {
            'time': datetime.now()
        },
        {
            'time': '19 марта',
        },
        {
            'time': '18 марта',
        },
        {
            'time': '17 марта',
        }
    ]

    posts = [
        {
            'author': {'username': 'John'},
            'body': 'John = 100 <br><br>Susan = 200 \n Иполит = 300'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'John = 100 \n Susan = 200 \n Иполит = 300'
        },
        {
            'author': {'username': 'Иполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]

    return render_template('index.html', title='Paybot', posts=posts, dates=dates)