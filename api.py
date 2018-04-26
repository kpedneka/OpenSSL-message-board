#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 19:11:40 2018

@author: nandan
"""
import os
import errno
import datetime
path = os.getcwd() + '/groups/'
def put_messages(group, username, message):
    requested_path = path + group
    if os.path.commonprefix((os.path.realpath(requested_path),path)) != path:
        print 'Preventing directory traversal'
        return

    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    fo = open(path+group, "a+")
    fo.seek(0,2)
    
    fo.write("Date: " +datetime.datetime.now().strftime("%A %d %B %Y %I:%M %p")+", User:"+username+ " , Message : " + message + "\n")
    fo.close()


def get_messages(group):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
        
    try:
        fp = open(os.path.join(path,group), "r+")
    except IOError:
        print ('cannot open', path+group)
        return []
    data_list = fp.read()
    #for line in fp:
        #data_list.append(tuple(line.strip().split("\",\"")))
    #fp.close()
    return data_list

def get_groups():
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return onlyfiles
