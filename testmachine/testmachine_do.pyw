# _*_ coding:utf-8 _*_
# Filename:ClientUI.py
# Python在线聊天客户端

from Tkinter import *
import Tkinter
import tkFont
import socket
import thread
import time
import sys
import urllib2,urllib
from xml.etree import ElementTree
import random,uuid,time,datetime
#import demo
import xiaoi.ibotcloud
import sendpost
class ClientUI():
    #global flag
    #global userstr
    userstr=""
    flag=True
    title = '机器人客户端'
    #local = '127.0.0.1'
    #port = 8808
    #global clientSock;
    #flag = False

    #初始化
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title(self.title)

        #窗口面板,用4个面板布局
        self.frame = [Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame(),Tkinter.Frame()]

        #显示消息Text右边的滚动条
        self.chatTextScrollBar = Tkinter.Scrollbar(self.frame[0])
        self.chatTextScrollBar.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)

        #显示消息Text，并绑定上面的滚动条
        ft = tkFont.Font(family='Fixdsys',size=11)
        #root = Tk()

        #self.chatText = Tkinter.Listbox(self.frame[0],width=70,height=18,font=ft)
        self.chatText=Tkinter.Text(self.frame[0],width=70,height=25,font=ft)
        self.chatText['yscrollcommand'] = self.chatTextScrollBar.set
        self.chatText.pack(expand=1,fill=Tkinter.BOTH)
        #self.chatText(root,warplength=80).pack()
        self.chatTextScrollBar['command'] = self.chatText.yview()
        self.frame[0].pack(expand=1,fill=Tkinter.BOTH)


        label = Tkinter.Label(self.frame[1],height=2,text="用时")
        label.pack(fill=Tkinter.BOTH,side=Tkinter.LEFT)
        #label.pack(fill=Tkinter.BOTH,3,1)
        self.frame[1].pack(expand=1,fill=Tkinter.BOTH)

        

        #self.inputTextScrollBar = Tkinter.Scrollbar(self.frame[2])
        #self.inputTextScrollBar.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)

        #ft = tkFont.Font(family='Fixdsys',size=11)
        #self.chatText1 = Tkinter.Listbox(self.frame[2],width=70,height=2,font=ft)
        #self.chatText1['yscrollcommand'] = self.chatTextScrollBar.set
        #self.chatText1.pack(expand=1,fill=Tkinter.BOTH)
        #self.chatTextScrollBar['command'] = self.chatText.yview()
        #self.frame[2].pack(expand=1,fill=Tkinter.BOTH)

        
        #显示指令以及用时
        ft = tkFont.Font(family='Fixdsys',size=11)
        self.chatText1 = Tkinter.Listbox(self.frame[2],width=70,height=1,font=ft)
        self.chatText1.pack(expand=1,fill=Tkinter.BOTH)
        self.frame[2].pack(expand=1,fill=Tkinter.BOTH)
        #输入用户id
        label = Tkinter.Label(self.frame[3],height=2,text="用户id")
        label.pack(fill=Tkinter.BOTH,side=Tkinter.LEFT)
        #label.pack(fill=Tkinter.BOTH,3,1)
        self.frame[3].pack(expand=1,fill=Tkinter.BOTH)

        ft = tkFont.Font(family='Fixdsys',size=11)
        self.inputText1 = Tkinter.Text(self.frame[4],width=70,height=1,font=ft)
        self.inputText1.pack(expand=1,fill=Tkinter.BOTH)
        self.frame[4].pack(expand=1,fill=Tkinter.BOTH)

        #输入用户密码
        label = Tkinter.Label(self.frame[5],height=2,text="用户密码")
        label.pack(fill=Tkinter.BOTH,side=Tkinter.LEFT)
        #label.pack(fill=Tkinter.BOTH,3,1)
        self.frame[5].pack(expand=1,fill=Tkinter.BOTH)

        ft = tkFont.Font(family='Fixdsys',size=11)
        self.inputText2 = Tkinter.Text(self.frame[6],width=70,height=1,font=ft)
        self.inputText2.pack(expand=1,fill=Tkinter.BOTH)
        self.frame[6].pack(expand=1,fill=Tkinter.BOTH)
        
        label = Tkinter.Label(self.frame[7],height=2,text="问句:")
        label.pack(fill=Tkinter.BOTH,side=Tkinter.LEFT)
        #label.pack(fill=Tkinter.BOTH,3,1)
        self.frame[7].pack(expand=1,fill=Tkinter.BOTH)
        #self.frame[1].LabelText="answer"
        #输入消息Text的滚动条
        self.inputTextScrollBar = Tkinter.Scrollbar(self.frame[8])
        self.inputTextScrollBar.pack(side=Tkinter.RIGHT,fill=Tkinter.Y)
        
        #输入消息Text，并与滚动条绑定
        ft = tkFont.Font(family='Fixdsys',size=11)
        self.inputText = Tkinter.Text(self.frame[8],width=70,height=5,font=ft)
        self.inputText['yscrollcommand'] = self.inputTextScrollBar.set
        self.inputText.pack(expand=1,fill=Tkinter.BOTH)
        self.inputTextScrollBar['command'] = self.chatText.yview()
        self.frame[8].pack(expand=1,fill=Tkinter.BOTH)

        #发送消息按钮
        self.sendButton=Tkinter.Button(self.frame[9],text=' 发 送 ',width=10,command=self.sendmessage_do)
        #self.sendButton.pack(expand=1,side=Tkinter.BOTTOM and Tkinter.LEFT,padx=15,pady=8)
        self.sendButton.pack(expand=1,side=Tkinter.LEFT,padx=15,pady=8)
        #关闭按钮
        self.closeButton=Tkinter.Button(self.frame[9],text=' 关 闭 ',width=10,command=self.close)
        self.closeButton.pack(expand=1,side=Tkinter.RIGHT,padx=15,pady=8)

        self.flashButton=Tkinter.Button(self.frame[9],text=' 刷新 ',width=10,command=self.flash)
        self.flashButton.pack(expand=1,side=Tkinter.RIGHT,padx=15,pady=8)
        self.frame[9].pack(expand=1,fill=Tkinter.BOTH)

    #接收消息
    '''
    def receiveMessage(self):
        try:
            #建立Socket连接
            self.clientSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.clientSock.connect((self.local, self.port))
            self.flag = True
        except:
            self.flag = False
            self.chatText.insert(Tkinter.END,'您还未与服务器端建立连接，请检查服务器端是否已经启动')
            return

        self.buffer = 1024
        self.clientSock.send('Y')
        while True:
            try:
                if self.flag == True:
                    #连接建立，接收服务器端消息
                    self.serverMsg = self.clientSock.recv(self.buffer)
                    if self.serverMsg == 'Y':
                        self.chatText.insert(Tkinter.END,'客户端已经与服务器端建立连接......')
                    elif self.serverMsg == 'N':
                        self.chatText.insert(Tkinter.END,'客户端与服务器端建立连接失败......')
                    elif not self.serverMsg:
                        continue
                    else:
                        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        self.chatText.insert(Tkinter.END, '服务器端 ' + theTime +' 说：\n')
                        self.chatText.insert(Tkinter.END, '  ' + self.serverMsg)
                else:
                    break
            except EOFError, msg:
                raise msg
                self.clientSock.close()
                break

    #发送消息
    def sendMessage(self):
        #得到用户在Text中输入的消息
        message = self.inputText.get('1.0',Tkinter.END)
        #格式化当前的时间
        theTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.chatText.insert(Tkinter.END, '客户端器 ' + theTime +' 说：\n')
        self.chatText.insert(Tkinter.END,'  ' + message + '\n')
        if self.flag == True:
            #将消息发送到服务器端
            self.clientSock.send(message);
        else:
            #Socket连接没有建立，提示用户
            self.chatText.insert(Tkinter.END,'您还未与服务器端建立连接，服务器端无法收到您的消息\n')
        #清空用户在Text中输入的消息
        self.inputText.delete(0.0,message.__len__()-1.0)

    #关闭消息窗口并退出
    def close(self):
        sys.exit()

    #启动线程接收服务器端的消息
    def startNewThread(self):
        #启动一个新线程来接收服务器端的消息
        #thread.start_new_thread(function,args[,kwargs])函数原型，
        #其中function参数是将要调用的线程函数，args是传递给线程函数的参数，它必须是个元组类型，而kwargs是可选的参数
        #receiveMessage函数不需要参数，就传一个空元组
        thread.start_new_thread(self.receiveMessage,())

    def flash(self):
        self.flag=False
        print self.flag
    def close(self):
        sys.exit()

    def sendMessage(self):
        message=self.inputText.get('1.0',Tkinter.END)
        tranmessage=message.encode("utf-8")
        urlstr="http://i.xiaoi.com/robot/ask.action?userId=%s&platform=web&"
        if self.userstr=="":
            self.userstr="task_tester"
        #userstr=str(uuid.uuid1())+str(random.random())
        if not self.flag:
            self.userstr=str(uuid.uuid1())+str(random.random())
            #self.chatText.delete()
            self.flag=True
        #else:
            #userstr=
        print self.flag
        urlstr=urlstr%(self.userstr)
        testurl=urlstr+urllib.urlencode({"question":tranmessage})
        req=urllib2.Request(url=testurl)
        print req
        print urlstr
        print message.encode("utf-8")
        start_time=datetime.datetime.now()
        res=urllib2.urlopen(req)
        end_time=datetime.datetime.now()
        span_time=end_time-start_time
        respage=res.read()
        root=ElementTree.fromstring(respage)
        #command=root.findall("Command")
        content=root.getiterator("Content")
        command=root.getiterator("Command")
        if len(command)>0:
            command_list=dict(command[0].attrib)
            try:
                command_server=command_list["name"]
            except:
                command_server="none"
                print command_list[0]
        else:
            command_server="none"
        print command_server
        #commanding=command["Command"]
        #print commanding["name"]

        print content
        #for i in content:
        if len(content)==0:
            content=""
        else:
            content=content[0].text
            #content=i.text
        #print content.decode("string_escape")
        print content.encode("gb18030"),"23333333333"
        self.chatText.delete(0.0,END)
        self.chatText.insert(Tkinter.END,"问句："+message.encode("utf-8")+"\n")
        self.chatText.insert(Tkinter.END,"机器人："+content.encode("utf-8")+"\n")
        try:
            self.chatText1.delete(0,END)
            #self.chatText1.delete(0,END)
            #self.chatText1.insert(Tkinter.END,"服务指令："+command_server.encode("utf-8")+"\n"+"用时："+str(span_time))
            self.chatText1.insert(Tkinter.END,"服务指令："+command_server.encode("utf-8"))
            self.chatText1.insert(Tkinter.END,"用时："+str(span_time))
            print"122222222222222222222"

        except:
            #self.chatText1.insert(Tkinter.END,"服务指令："+command_server.encode("utf-8")+"\n"+"用时："+str(span_time))
            #self.chatText1.insert(Tkinter.END,"服务指令："+command_server.encode("utf-8"))
            #self.chatText1.insert("用时："+str(span_time))
            #print"21111111111111111111111111"
            self.chatText1.insert(Tkinter.END,"failed")
        self.inputText.delete(0.0,message.__len__()-1.0)
        print self.userstr
'''
    #刷新user_id
    def flash(self):
        self.flag=False
        print self.flag
    #关闭页面 
    def close(self):
        sys.exit()

    #调取回复模块
    def get_theanswer(self,question):
        input_id=self.inputText1.get('1.0',Tkinter.END)
        input_password=self.inputText2.get('1.0',Tkinter.END)
        tran_input_id=input_id.strip()
        tran_input_password=input_password.strip()
        get_key_sec=sendpost.sendpost_mod("http://cloud.xiaoi.com/user/developer/developer!index.do",tran_input_id,tran_input_password)
        print input_id,input_password,get_key_sec
        test_key=get_key_sec[0]
        test_sec=get_key_sec[1]
        signature_ask = xiaoi.ibotcloud.IBotSignature(app_key=test_key,
                                              app_sec=test_sec,
                                              uri="/ask.do",
                                              http_method="POST")
        if self.userstr=="":
            self.userstr="task_tester"
        #userstr=str(uuid.uuid1())+str(random.random())
        if not self.flag:
            self.userstr=str(uuid.uuid1())+str(random.random())
            #self.chatText.delete()
            self.flag=True
        #else:
            #userstr=
        print self.flag
        params_ask = xiaoi.ibotcloud.AskParams(platform="custom",
                                       user_id=self.userstr,
                                       url="http://nlp.xiaoi.com/ask.do",
                                       response_format="xml")
        ask_session = xiaoi.ibotcloud.AskSession(signature_ask, params_ask)

    #def get_answer_do(self,question):
        #self.get_keyandsec
        
        ret_answer=ask_session.get_answer(question)
        return ret_answer

    #发送问题模块，并结果显示 
    def sendmessage_do(self):
        '''
        input_id=self.inputText1.get('1.0',Tkinter.END)
        input_password=self.inputText2.get('1.0',Tkinter.END)
        get_key_sec=sendpost_mod("http://cloud.xiaoi.com/user/developer/developer!index.do",input_id,input_password)
        #import demo
        #demo.test_key=get_key_sec[0]
        #demo.test_sec=get_key_sec[1]
        test_key=get_key_sec[0]
        test_sec=get_key_sec[1]
        signature_ask = xiaoi.ibotcloud.IBotSignature(app_key=test_key,
                                              app_sec=test_sec,
                                              uri="/ask.do",
                                              http_method="POST")
        
        if self.userstr=="":
            self.userstr="task_tester"
        #userstr=str(uuid.uuid1())+str(random.random())
        if not self.flag:
            self.userstr=str(uuid.uuid1())+str(random.random())
            #self.chatText.delete()
            self.flag=True
        #else:
            #userstr=
        print self.flag
        params_ask = xiaoi.ibotcloud.AskParams(platform="custom",
                                       user_id=self.userstr,
                                       url="http://nlp.xiaoi.com/ask.do",
                                       response_format="xml")
        ask_session = xiaoi.ibotcloud.AskSession(signature_ask, params_ask)
        '''
        input_message=self.inputText.get('1.0',Tkinter.END)
        #qst=input_message.decode("gb18030").encode("utf-8")
        start_time=datetime.datetime.now()
        get_the_answer=self.get_theanswer(input_message.encode("utf-8"))
        end_time=datetime.datetime.now()
        time_span=end_time-start_time
        print get_the_answer.http_body
        self.chatText.delete(0.0,END)
        self.chatText.insert(Tkinter.END,"问句："+input_message.encode("utf-8")+"\n")
        self.chatText.insert(Tkinter.END,"机器人："+get_the_answer.http_body+"\n")
        try:
            self.chatText1.delete(0,END)
            #self.chatText1.delete(0,END)
            #self.chatText1.insert(Tkinter.END,"服务指令："+command_server.encode("utf-8")+"\n"+"用时："+str(span_time))
            #self.chatText1.insert(Tkinter.END,"服务指令："+command_server.encode("utf-8"))
            self.chatText1.insert(Tkinter.END,"用时："+str(time_span))
            #print"122222222222222222222"

        except:
            #self.chatText1.insert(Tkinter.END,"服务指令："+command_server.encode("utf-8")+"\n"+"用时："+str(span_time))
            #self.chatText1.insert(Tkinter.END,"服务指令："+command_server.encode("utf-8"))
            #self.chatText1.insert("用时："+str(span_time))
            #print"21111111111111111111111111"
            self.chatText1.insert(Tkinter.END,"failed")
        self.inputText.delete(0.0,input_message.__len__()-1.0)
        
def main():
    client = ClientUI()
    #client.startNewThread()
    client.root.mainloop()

if __name__=='__main__':
    main()
