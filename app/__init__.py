#!python
#coding:utf-8

import sqlite3
from flask import Flask,request
from flask_cors import CORS
import json

app = Flask(__name__)

from app import router

# 跨域
CORS(app, resources=r'/*')


