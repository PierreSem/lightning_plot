from flask import Flask, render_template, json, request, redirect, url_for,\
     flash
import numpy as np
from sp_lightning import read_signal_txt, read_signal_fms

import matplotlib
import json
import random
import os

#matplotlib.use('Agg')
import matplotlib.pyplot as plt
#plt.ioff()
import mpld3
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = set(['txt', 'fms'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in\
           ALLOWED_EXTENSIONS

def graph_test(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    fig_html = mpld3.fig_to_html(fig)
    plt.close()
    return fig_html



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('index.html', filename = filename)
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/query/<filename>')
def query(filename):
    if filename.find('.txt') <> -1:
        x, y = read_signal_txt(filename)
    elif filename.find('.fms') <> -1:
        x, y = read_signal_fms(filename)
    fig_html = graph_test(x, y)
    return fig_html


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
