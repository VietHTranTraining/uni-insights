from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import document_utils

import json
import os
import random
import re
import time

from review_analysis import analyze_essay, analyze_twitter

app = Flask(__name__, template_folder='templates')
TRAINED_MEMORY_FILE = './trained_memory.json'
DIRECTORY_FILE_NAME = './id_name.json'
TRAINED_DATA = None
ID_NAME = None

def init_data():
    if TRAINED_DATA is not None:
        return
    global TRAINED_DATA, ID_NAME
    TRAINED_DATA = document_utils.read_json(TRAINED_MEMORY_FILE)
    ID_NAME = document_utils.read_json(DIRECTORY_FILE_NAME)

@app.route('/', methods=['GET'])
def home():
    init_data()
    universities = [k for k in TRAINED_DATA['essay']]
    return render_template('index.html', universities=universities)

@app.route('/twitter', methods=['GET'])
def home_twitter():
    init_data()
    universities = [k for k in TRAINED_DATA['twitter']]
    return render_template('twitter_index.html', universities=universities)

@app.route('/analyze_result', methods=['POST'])
def analyze_user():
    init_data()
    score, message = analyze_essay(request.form['essay'].encode('ascii', 'ignore'), request.form['university'])    
    return render_template('match_score_essay.html',
            score=round(score * 100, 2),
            message=message,
            id_name=ID_NAME,
            university=request.form['university'],
            method='Essay')

@app.route('/analyze_result_twitter', methods=['POST'])
def analyze_user_twitter():
    init_data()
    score, message = analyze_twitter(request.form['twitter'].encode('ascii', 'ignore'), request.form['university'])    
    return render_template('match_score_twitter.html',
            score=round(score * 100, 2),
            message=message, id_name=ID_NAME,
            university=request.form['university'],
            method='Twitter')

@app.route('/university', methods=['get'])
def select_university():
    init_data()
    universities = [k for k in TRAINED_DATA['essay']]
    return render_template('select_university.html', universities=universities)

@app.route('/insights', methods=['post'])
def get_university_data():
    init_data()
    university = request.form['university']
    score, message_essay = analyze_essay(document_utils.read_text_file('./test_essay.txt'), request.form['university'])    
    score, message_twitter = analyze_twitter('penn_state', request.form['university'])    
    return render_template('get_university_data.html',
            message_essay=message_essay,
            message_twitter=message_twitter,
            id_name=ID_NAME,
            university=university)

port = int(os.getenv('PORT', 8000))

if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = '0.0.0.0', port = port)
