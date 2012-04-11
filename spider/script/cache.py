'''
Created on 2011-12-20

@author: lds
'''
import md5
import os
import pickle

def _makeFileName(id):
    return os.path.dirname(__file__) + '/' + str(id)

def cache(object, id=None):
    if not id:
        id = MD5(object)
    output = open(_makeFileName(id), 'wb')
    pickle.dump(object, output)
    output.close()
    
def has_cache(id):
    #print 'check cache :' + _makeFileName(id)
    return os.path.isfile(_makeFileName(id))
    
def load(id):
    input = open(_makeFileName(id), 'rb')
    data = pickle.load(input)
    input.close()
    return data

def MD5(object):
    m = md5.new()
    m.update(object)
    return m.digest()

