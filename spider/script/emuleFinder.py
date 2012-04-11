#- coding: utf-8
'''
Created on 2011-12-20

@author: lds
'''
from Spider import Spider, FormAuth
import cache


'''
step 1: get HTML page source
step 2: parse HTML string for ed2k links(link and filename)
step 3: search filename for 'S00E00', now we got {link, filename, episode}
step 4: store into database.(怎么高效分析出得到的所有links中哪些是还没有存入数据库的（即防止重复数据）
sus: cache the last time links list and compare them to the new one
'''
def main():
    ydyFinder()
    yyetsFinder()

def ydyFinder():
    # everything for login
    username = 'lds1129'
    password = '19851129'
    auth_data = {'username': username,
                 'password': password,
                 'formhash':'592862ac'}
    login_page = 'http://bbs.sfile2012.com/logging.php?action=login&loginsubmit=yes'
    auth = FormAuth(auth_data, login_page)
    
    # good hunting
    urls = ['http://bbs.sfile2012.com/viewthread.php?tid=351496&extra=page%3D1', # BONES
            'http://bbs.sfile2012.com/viewthread.php?tid=348582&extra=page%3D1', # HOUSE
            'http://bbs.sfile2012.com/viewthread.php?tid=348117&extra=page%3D1', # MENTALIST
            ]
    spider = Spider(urls, auth)
    spider.start()
    
def yyetsFinder():
    urls = ['http://yyets.com/showresource-juji-1103.html'  # 2 BROKE GIRlS
            ,'http://yyets.com/showresource-juji-1088.html' # HOMELAND
            ,'http://yyets.com/showresource-juji-1007.html' # MENTALIST
            ,'http://yyets.com/showresource-juji-974.html'  # NEW GIRL
            ] 
    spider = Spider(urls)
    spider.start()

if __name__ == '__main__':
    main()
