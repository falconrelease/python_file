'''import unicode
str = "\xbe\xdc\xbe\xf8\xb7\xc3\xce\xca\xa1\xa3"
b = repr(str)
print (unicode(eval(b),"gbk"))
'''

a = "\xb3\xc2\xbd\xa8\xc3\xf4"
a=str.encode(str(a))
print(a)
b = a.decode('gbk')

print (b)
import logging  
logging.debug('debug message')  
logging.info('info message')  
logging.warning('warning message')  
logging.error('error message')  
logging.critical('critical message')  
