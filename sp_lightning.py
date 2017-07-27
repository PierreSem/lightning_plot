from os import popen
from numpy import loadtxt
from time import gmtime, mktime
from datetime import datetime

def read_signal_txt(filename):
    tab = []
    tab = loadtxt('data/' + filename)
    tmp = 0
    x = []
    y = []
    try:
        dim = len(tab[0])
    except TypeError:
        dim = 1
    for i in tab :
        if dim == 1:
            x.append(tmp)
            tmp = tmp + 1
            y.append(i)
        if dim ==2:
            x.append(i[0])
            y.append(i[1])
    return x, y, {} 

def read_signal_fms(filename):
    tab_tmp = popen('./flash2txt -s data/' + filename).readlines()
    #hd_tmp = popen('./flash2txt -H data/' + filename).readlines()
    param = read_parameter_fms(filename)
    print param
    dt = 1 / float(param['sampling_rate'])
    #dt = 1 / float(hd_tmp[1].split(':')[1])
    ind = int(param['ind'])
    tab = []
    for i in tab_tmp :
        tab.append(float(i))
    tmp = 0
    x = []
    y = []
    try:
        dim = len(tab[0])
    except TypeError:
        dim = 1
    for i in tab :
        if dim == 1:
            x.append((tmp - ind) * dt)
            tmp = tmp + 1
            y.append(i)
        if dim ==2:
            x.append(i[0])
            y.append(i[1])
    param = read_parameter_fms(filename)
    return x, y, param

def read_parameter_fms(filename):
    hd_tmp = popen('./flash2txt -H data/' + filename).readlines()
    print hd_tmp
    dt = 1 / float(hd_tmp[1].split(':')[1])
    epoch = hd_tmp[0].split(':')[1].rstrip('\n')
    date = int(float(epoch)) 
    second = float('0.' + epoch.rstrip('\n').split('.')[1])
    date = gmtime(date)
    print date, second
    print str(date.tm_mday) + '/' + str(date.tm_mon) + '/' + \
          str(date.tm_year) + ' ' + str(date.tm_hour) + ':' + \
          str(date.tm_min) + ':' + str(date.tm_sec + second)
    sampling_rate = float(hd_tmp[1].split(':')[1])
    channel = int(hd_tmp[2].split(':')[1])
    ind = int(hd_tmp[3].split(':')[1])
    fall_time = float(hd_tmp[4].split(':')[1])
    tpz = float(hd_tmp[5].split(':')[1])
    A = int(hd_tmp[6].split(':')[1])
    no_repetion = int(hd_tmp[7].split(':')[1])
    saturation = int(hd_tmp[8].split(':')[1])
    type_sig = int(hd_tmp[9].split(':')[1])
    parameter_sig = {'date' : epoch, 'sampling_rate' : sampling_rate,\
                     'channel' : channel, 'ind' : ind, 'fall_time': fall_time,\
                     'tpz' : tpz, 'A': A, 'no_repetion' : no_repetion,\
                     'saturation': saturation, 'type_sig' : type_sig}
    return parameter_sig
