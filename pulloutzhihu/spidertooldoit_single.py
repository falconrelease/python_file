#coding:utf-8
import urlinformation,urllib2,time,re,urllib
import xlrd
import xlwt
import sys
import logging
#from concurrent.futures import ThreadPoolExecutor

def decoratetool(rep_str):
    def _warpertool(func):
        def warpertool(*args):
            content=func(*args)
            repcontent=content.replace(rep_str,"")
            repcontent=repcontent.replace(" ","")
            return repcontent
        return warpertool
    return _warpertool

@decoratetool("<em>")
def repagain(findquestion):
    repquestion=findquestion.replace("</em>","")
    return repquestion

def openfile():
    filecontent=xlrd.open_workbook("remainpullout.xlsx")
    firstpage=filecontent.sheets()[0]
    runarray=firstpage.col_values(0)
    return runarray

def apply_url(qs):
    marknumber=0
    question=qs
    thisquestionextend=[]
    while marknumber<15:
        tranworkurlstr=urlinformation.formalurl
        #print tranworkurlstr,"22222222222"
        tranworkurl=tranworkurlstr%(marknumber,question.encode("utf-8"))
        print tranworkurl
        try:
            openpage=urllib2.urlopen(tranworkurl)
            #print "12342315215"
            openpagecontent=openpage.read()
            #print openpagecontent,"11111111111111111"
            buildruler=re.compile(r'target="_blank" class="ti">(.*?)</a>')
            selectstr=re.findall(buildruler,openpagecontent)
           
            for eachone in selectstr:
                #print eachone,"3333333333"
                eachonerep=repagain(eachone)
                print eachonerep
                thisquestionextend.append([question,eachonerep.decode("gb18030")])
        except Exception,e:
            thisquestionextend.append([question,"sorry on extend question"])
        marknumber+=10
    return thisquestionextend
class classfyexcel(object):
    def __init__(self):
        self.openfile=xlwt.Workbook()
        self.sheet1=self.openfile.add_sheet(u'首页',cell_overwrite_ok=True)
        self.rowsTitle=[u'标准问',u'扩展问']
        for i in range(0,len(self.rowsTitle)):
            self.sheet1.write(0,i,self.rowsTitle[i],self.set_style("Times new Roman",220,True))
        self.openfile.save('baiduzhidao.xls')
        logging.info("初始化文件结束")
        
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
    '''
    with ThreadPoolExecutor(max_workers=urlinformation.threadnumber) as executoring:
        for eachquestion,result in zip(questionlist,executoring.map(apply_url,questionlist)):
            for eachline in result:
                print (eachline[0],eachline[1])
                writescript.sheet1.write(mark,0,eachline[0])
                writescript.sheet1.write(mark,1,eachline[0])
                mark+=1
    '''
    answerboxlist=[apply_url(qs) for qs in questionlist]
    for eachresult in answerboxlist:
        for eachline in eachresult:
            print (eachline[0],eachline[1],"111111111111")
            try:
                writescript.sheet1.write(mark,0,eachline[0])
                #answer=
                writescript.sheet1.write(mark,1,eachline[1])
            except:
                writescript.sheet1.write(mark,0,eachline[0])
                writescript.sheet1.write(mark,1,"error")
            mark+=1
    
    writescript.openfile.save('baiduzhidao.xls')
                
