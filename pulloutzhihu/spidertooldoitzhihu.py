#coding:utf-8
import urlinformation,time,re
import xlrd
import xlwt
import sys
import logging
from urllib import request,parse
import requests,json
from concurrent.futures import ThreadPoolExecutor

def decoratetool(rep_str):
    def _warpertool(func):
        def warpertool(*args):
            content=func(*args)
            repcontent=content.replace(rep_str,"")
            return repcontent
        return warpertool
    return _warpertool

@decoratetool("<em>")
def repagain(findquestion):
    repquestion=findquestion.replace("</em>","")
    return repquestion

#导入问句
def openfile():
    questionlistarray=[]
    filecontent=xlrd.open_workbook("remainpullout.xlsx")
    firstpage=filecontent.sheets()[0]
    runarray=firstpage.col_values(0)
    for eachstr in runarray:
        questionlistarray.append([eachstr,str(eachstr)])
    return questionlistarray

#调用请求返回结果                                 
def apply_url(qs):
    marknumber=0
    question=qs[1]
    thisquestionextend=[]
    while marknumber<20:
        tranworkurlstr=urlinformation.formalurl
        tranworkurl=tranworkurlstr%(marknumber)
        tranworkurl=tranworkurl+parse.urlencode({"q":question})
        print(tranworkurl)
        headers = {
            'accept': 'application/json, text/plain, */*',
            # 'Accept-Encoding':'gzip, deflate, sdch, br',
            # 'Accept-Language':'zh-CN,zh;q=0.8',
            'authorization': 'Bearer 2|1:0|10:1517461526|4:z_c0|80:MS4xNUNPVEJ3QUFBQUFtQUFBQVlBSlZUUmJ1WDF2MUpEM2FPTDFWUHhaYkUyalFLVGJ5NmxyMW13PT0=|eb55adf81bace1838be0828e017353601fa152359b566bb5f57d3c35436b3696',
            'Connection': 'keep-alive',
            'Cookie': 'q_c1=8020fc8dc8f74bffade1741c15481181|1517302608000|1517302608000; _zap=07fffc3b-2b46-4fe5-a295-442a1ccd05e9; r_cap_id="ZWY4MjBkOGM3ZmY0NGEwMDgzMDk2NmU3ZGZjMDYwMTQ=|1517302631|91232c84c615cff5c905f9175bbfc013a1de7f83"; cap_id="YmYyNzI4MTRlMGNjNGYxZDgxNDBlMDY4NTM1NTdhNDk=|1517302631|e3f1e379146d25269ffffb587657e84938cdf5a8"; l_cap_id="YjQ1ZGQ0ZmY0NzJmNGMzOTgzMjNmYTY3M2IyMjdlOGI=|1517302631|393fc908a6d42e8df93c41806941c3105096753a"; __utma=155987696.1130644517.1517461401.1517461401.1517461401.1; __utmz=155987696.1517461401.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); capsion_ticket="2|1:0|10:1517461503|14:capsion_ticket|44:NjE4ZWVlODViODkyNDI2OTlhYTQ2MjQ4NmE5Yjk4ZTM=|36c7376a40cfac905059ae5ee57154124ace89c2b72b054925a4584c0c5835bb"; z_c0="2|1:0|10:1517461526|4:z_c0|80:MS4xNUNPVEJ3QUFBQUFtQUFBQVlBSlZUUmJ1WDF2MUpEM2FPTDFWUHhaYkUyalFLVGJ5NmxyMW13PT0=|eb55adf81bace1838be0828e017353601fa152359b566bb5f57d3c35436b3696"; aliyungf_tc=AQAAANjwPyHu3AIA+gP43HXJRHRp+/XP; _xsrf=b46c2275-92f0-4829-b83a-31cd432d7428',
            # 'Host':'www.zhihu.com',
            'Referer': 'https://www.zhihu.com/search?type=content&q=%E5%8F%98%E5%BD%A2%E9%87%91%E5%88%9A%E6%80%8E%E4%B9%88%E6%A0%B7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'x-api-version': '3.0.91',
            'x-app-za': 'OS=Web'
        }
        try:
            page = requests.get(url=tranworkurl, headers=headers)
            dict_list = page.json()
            
            for i in range(len(dict_list['data'])):
                try:
                    questionstr = dict_list['data'][i]['object']['question']['name']
                    #print(questionstr)
                    questionstr=repagain(questionstr)
                
                    thisquestionextend.append([qs[0],questionstr])
                    print("this string is:{}".format(questionstr))
                except:
                    next
        except Exception as e:
            thisquestionextend.append([question,"sorry on extend question"])
        marknumber+=10
    return thisquestionextend

#初始化结果文件
class classfyexcel(object):
    def __init__(self):
        self.openfile=xlwt.Workbook()
        self.sheet1=self.openfile.add_sheet(u'首页',cell_overwrite_ok=True)
        self.rowsTitle=[u'标准问',u'扩展问']
        for i in range(0,len(self.rowsTitle)):
            self.sheet1.write(0,i,self.rowsTitle[i],self.set_style("Times new Roman",220,True))
        self.openfile.save('baiduzhidao.xls')
        logging.warning("初始化文件结束")

    def set_style(self,name,height,bold=False):
        style=xlwt.XFStyle()
        font=xlwt.Font()
        font.name=name
        font.height=height
        font.color_index=2
        font.bold=bold
        style.font=font
        return style
if '_main_':
    writescript=classfyexcel()
    #writefile=xlrd.open_workbook('baiduzhidao.xls')
    #writefile.sheet1=writefile.sheets()[0]
    questionlist=openfile()
    mark=1
    start=time.time()
    #调用线程池进行爬取
    with ThreadPoolExecutor(max_workers=urlinformation.threadnumber) as executoring:
        for eachquestion,result in zip(questionlist,executoring.map(apply_url,questionlist)):
            for eachline in result:
                print("当前写入标准问：{}，写入扩展问：{}".format(eachline[0],eachline[1]))
                writescript.sheet1.write(mark,0,eachline[0])
                writescript.sheet1.write(mark,1,eachline[1])
                mark+=1
    logging.warning("爬取结束！！！，用时：{:2f}".format(time.time()-start))
    writescript.openfile.save('baiduzhidao.xls')
    
