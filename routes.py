from flask import Flask, render_template, json, request
import numpy as np

import matplotlib
import json
import random

#matplotlib.use('Agg')
import matplotlib.pyplot as plt
#plt.ioff()

import mpld3

app = Flask(__name__)



def graph_test():
    x = range(100)
    y = [a * 2 + random.randint(-20, 20) for a in x]
    fig, ax = plt.subplots()
    ax.plot(x, y)
    fig_html = mpld3.fig_to_html(fig)
    plt.close()
    return fig_html



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/query')
def query():
    fig_html = graph_test()
    return fig_html


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
