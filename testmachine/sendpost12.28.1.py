#coding:utf-8
import urllib2
import urllib
import cookielib,re
def sendpost_mod(url,userid,password):
    loginpage="http://cloud.xiaoi.com/login!user.do"
    #loginpage="http://cloud.xiaoi.com/login.jsp"
    try:
        example=cookielib.CookieJar()
        open_example=urllib2.build_opener(urllib2.HTTPCookieProcessor(example))
        open_example.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]

        data=urllib.urlencode({"loginInfo.nick":userid,"loginInfo.password":password})
        open_example.open(loginpage,data)
        open_page=open_example.open(url)
        data_source=open_page.read()
        
        #return data_source
    except Exception ,e:
        print "error"
    ruler2=re.compile(r'value="(.*?)">')
    key_sec=re.findall(ruler2,data_source)
    return key_sec
#print sendpost_mod("http://cloud.xiaoi.com/user/developer/developer!index.do","xiaoiid211","qwe123")
#resultstring=sendpost_mod("http://cloud.xiaoi.com/user/developer/developer!index.do","xiaoiid211","qwe123")
#ruler1=re.compile(r'value="(.*?)">')
#string1=re.findall(ruler1,resultstring)
#print string1
