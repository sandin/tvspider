#- coding: utf-8
import urllib, urllib2, cookielib
import sqlite3
import re
from BeautifulSoup import BeautifulSoup 

def getHTML(url):
    username = 'lds1129'
    password = '19851129'
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_data = urllib.urlencode({'username':username, 'password':password,'formhash':'592862ac'})
    resp = opener.open("http://bbs.sfile2012.com/logging.php?action=login&loginsubmit=yes", login_data)
    tmp = resp.read()
    print tmp
    response = opener.open(url)
    html = response.read()
    return html

####################################################
def findED2K(html):
    downloadList = []
    soup = BeautifulSoup(html)
    #print soup.prettify()
    emuleList = soup.find("ul", {'class':"emuledow"})
    for li_elem in emuleList.findAll('li'):
        input_elem = li_elem.find('input');
        ed2k = input_elem.get('value', '')
        if ed2k and ed2k.startswith('ed2k') and ed2k.find('------------') == -1:
            downloadList.append(ed2k)
    return downloadList

def saveData(list):
    conn = sqlite3.connect('ed2k.db')
    c = conn.cursor()
    #c.execute('''create table ed2k
    #(link text)''')
    for link in list:
        print "save data into db: " + link
        c.execute("insert into ed2k values ('" + link + "')")
    conn.commit()
    c.close()
########################################################

def main():
    url = "http://bbs.sfile2012.com/viewthread.php?tid=348117&extra=page%3D1"
    html = getHTML(url)
    #print html
    ed2kFileLinkRegex = re.compile(\
        '(ed2k://\|file\|(.+?)\|\d+\|[a-fA-F0-9]{32}\|' + \
        '(((p=[a-fA-F0-9]{32}(:[a-fA-F0-9]{32})*\|)?(h=\w{32}\|)?(s=http://[\w\.-_&%/]+\|)*)|' + \
        '((p=[a-fA-F0-9]{32}(:[a-fA-F0-9]{32})*\|)?(s=http://[\w\.-_&%/]+\|)*(h=\w{32}\|)?)|' + \
        '((h=\w{32}\|)?(p=[a-fA-F0-9]{32}(:[a-fA-F0-9]{32})*\|)?(s=http://[\w\.-_&%/]+\|)*)|' + \
        '((h=\w{32}\|)?(s=http://[\w\.-_&%/]+\|)*(p=[a-fA-F0-9]{32}(:[a-fA-F0-9]{32})*\|)?)|' + \
        '((s=http://[\w\.-_&%/]+\|)*(p=[a-fA-F0-9]{32}(:[a-fA-F0-9]{32})*\|)?(h=\w{32}\|)?)|' + \
        '((s=http://[\w\.-_&%/]+\|)*(h=\w{32}\|)?(p=[a-fA-F0-9]{32}(:[a-fA-F0-9]{32})*\|)?))' + \
        '/(\|sources,[\w\.-_]+:\d{1,5}\|/)?)')
    links = ed2kFileLinkRegex.findall(html)
    for l in links:
        print l
    
    #url = "http://yyets.com/showresource-juji-1030.html"
    #list = findED2K(getHTML(url))
    #saveData(list)


main()
