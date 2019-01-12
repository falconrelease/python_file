# -*- coding: utf-8 -*-

import xiaoi.ibotcloud
#import testmachine_do
import sendpost12.28.1
# please input your key/sec
test_key = "YOU_KEY"
test_sec = "YOU_SEC"

signature_ask = xiaoi.ibotcloud.IBotSignature(app_key=test_key,
                                              app_sec=test_sec,
                                              uri="/ask.do",
                                              http_method="POST")

signature_reg = xiaoi.ibotcloud.IBotSignature(app_key=test_key,
                                              app_sec=test_sec,
                                              uri="/recog.do",
                                              http_method="POST")

signature_tts = xiaoi.ibotcloud.IBotSignature(app_key=test_key,
                                              app_sec=test_sec,
                                              uri="/synth.do",
                                              http_method="POST")

params_tts = xiaoi.ibotcloud.TTSParams(url="http://vcloud.xiaoi.com/synth.do")
params_reg = xiaoi.ibotcloud.RegParams(url="http://vcloud.xiaoi.com/recog.do")
params_ask = xiaoi.ibotcloud.AskParams(platform="custom",
                                       user_id="abc",
                                       url="http://nlp.xiaoi.com/ask.do",
                                       response_format="xml")

ask_session = xiaoi.ibotcloud.AskSession(signature_ask, params_ask)
reg_session = xiaoi.ibotcloud.RegSession(signature_reg, params_reg)
tts_session = xiaoi.ibotcloud.TTSSession(signature_tts, params_tts)

# demo how to get answer
ret_ask = ask_session.get_answer("你好")

print ret_ask.http_status, ret_ask.http_body

# demo how to get reg speech using speex file
speex_data = open("data/test16k.spx", "rb").read()

ret_reg = reg_session.get_reg_result(speex_data)

print ret_reg.http_status, ret_reg.http_body

# defmo how to get speex audio from text
ret_tts = tts_session.get_tts_result("你好")

print ret_tts.http_status, len(ret_tts.http_body)

def get_answer_do(question):
    ret_answer=ask_session.get_answer(question)
    return ret_answer

