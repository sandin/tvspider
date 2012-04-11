#- coding: utf-8
'''
Created on 2011-12-20

@author: lds
'''
import cache
import cookielib
import re
import threading
import urllib
import urllib2

import pyperclip
from BeautifulSoup import BeautifulSoup

class Spider(threading.Thread):
    '''
    spider of ed2k links
    '''
    urls = []
    ed2k = []
    urlOpener = None
    needAuth = False
    auth_data = {}
    
    ed2kFileLinkRegex = re.compile(\
        '(ed2k://\|file\|(.+?)\|\d+\|[a-fA-F0-9]{32}\|' + \
        '(((p=[a-fA-F0-9]{32}(:[a-fA-F0-9]{32})*\|)?(h=\w{32}\|)?(s=http://[\w\.-_&%/]+\|)*)|' + \
        '((p=[a-fA-F0-9]{32}(:[a-fA-F0-9]{32})*\|)?(s=http://[\w\.-_&%/]+\|)*(h=\w{32}\|)?)|' + \
        '((h=\w{32}\|)?(p=[a-fA-F0-9]{32}(:[a-fA-F0-9]{32})*\|)?(s=http://[\w\.-_&%/]+\|)*)|' + \
        '((h=\w{32}\|)?(s=http://[\w\.-_&%/]+\|)*(p=[a-fA-F0-9]{32}(:[a-fA-F0-9]{32})*\|)?)|' + \
        '((s=http://[\w\.-_&%/]+\|)*(p=[a-fA-F0-9]{32}(:[a-fA-F0-9]{32})*\|)?(h=\w{32}\|)?)|' + \
        '((s=http://[\w\.-_&%/]+\|)*(h=\w{32}\|)?(p=[a-fA-F0-9]{32}(:[a-fA-F0-9]{32})*\|)?))' + \
        '/(\|sources,[\w\.-_]+:\d{1,5}\|/)?)')

    def __init__(self, urls, auth=None):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.urls = urls
        if auth:
            self.auth = auth
            self.needAuth = True         
        
    def openPage(self, url):
        '''
        Open a HTML page, return HTML source string
        '''
        self.maybeBuildUrlOpener()
        resp = self.urlOpener.open(url)
        html = resp.read()
        #print html
        return html
    
    def maybeBuildUrlOpener(self):
        if not self.urlOpener:
            if self.needAuth:
                self.urlOpener = self.auth.getAuthenticatedUrlOpener()
            else:
                self.urlOpener = urllib.FancyURLopener({})
     
    def run(self):
        for url in self.urls:
            self.findNewEd2k(url)
        #print '---------RESULT------------'
        #for link in self.ed2k:
        #    print link
        
    def findNewEd2k(self, url):
        '''
        find and cache all ed2k links on a page, but only return new links
        '''
        links = self.findEd2k(url)
        print 'found %i ed2k links' % len(links)
        self.ed2k.extend(links)
        cache_id = hash(url)
        if cache.has_cache(cache_id):
            cacheList = cache.load(cache_id)
            if cacheList == self.ed2k:
                print 'nothing change. ' + url
            else: 
                print 'you has new links ' + url
                newLinks = zip(*self.ed2k)[0]
                oldLinks = zip(*cacheList)[0]
                diff = list(set(newLinks).difference( set(oldLinks) )) # lists difference
                for link in diff:
                    print link
                    pyperclip.copy(link) # TODO
        else:
            print 'just cache the links ' + url
        cache.cache(self.ed2k, cache_id)
            
    def findEd2k(self, url):
        '''
        find all ed2k links on a page
        '''
        html = self.openPage(url)
        links = self.ed2kFileLinkRegex.findall(html)
        newLists = []
        for link in links: 
            if len(link) < 2:
                continue # wrong format 
            ed2k = link[0]
            filename = link[1]
            if ed2k and isinstance(ed2k, str) and ed2k.startswith('ed2k') and ed2k.find('--------') == -1:
                newLists.append([ed2k, filename])
        #print newLists
        return newLists
    
class FormAuth(object):
    '''
    login with form post
    '''
    urlOpener = None
    authenticated = False
    login_data = {}
    
    def __init__(self, login_data, login_page):
        self.login_data = login_data
        self.login_page = login_page
        
    def login(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        login_data = urllib.urlencode(self.login_data)
        response = opener.open(self.login_page, login_data)
        #print response.read() # for debug
        self.urlOpener = opener
        
    def getAuthenticatedUrlOpener(self):
        '''
        use the return opener you can access any page which need authenticated
        '''
        if not self.urlOpener:
            self.login()
        return self.urlOpener
    
class TVEd2k(object):
    '''
    TV showek2k link wrapper
    '''
    
    def __init__(self, link, filename, name=None, episode=None):
        self.link = link
        self.filename = filename
        self.name = name
        self.episode = episode
        
    def isComplete(self):
        '''
        has everything 
        '''
        return self.link and self.filename and self.name and self.episode
