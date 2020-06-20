#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:52:49 2020

@author: vovanthuong
"""

# Nhập thư viện cần thiết
import random
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from underthesea import word_tokenize
import speech_recognition as sr # Thu âm
from gtts import gTTS # Chuyển thành giộng GG
import playsound  # Phát âm
import sys

# Đọc dữ liệu mẫu
data= pd.read_excel('quang binh.xlsx')
stop_words= open("stopwords.words", "r").read()
stop_words= stop_words.splitlines()

# Chuẩn hóa ký tự trong dữ liệu huấn luyện
def standardized_sentence(sentence):
    sentence= word_tokenize(sentence.lower(), format="text")
    return sentence

sample_questions= data.QUESTION
sample_questions= sample_questions.apply(standardized_sentence)
sample_questions= list(sample_questions)

sample_answer= list(data.ANSWER)

# Mô hình dự đoán
tfidf_vectorizer = TfidfVectorizer(stop_words= ['quảng_bình']).fit(sample_questions)
tfidf = tfidf_vectorizer.transform(sample_questions)

# Phản hồi đối với câu hỏi
def response(question_input):
    # Chuẩn hóa ký tự trong câu hỏi nhập vào
    question_input= standardized_sentence(question_input)
    question_input= [question_input]   
    # Tính tfidf với câu hỏi nhập vào
    tfidf_input= tfidf_vectorizer.transform(question_input)
    # Tính toán độ giống nhau của câu nhập vào và câu hỏi mẫu
    vals = cosine_similarity(tfidf_input, tfidf)
    vals= vals.flatten()
    max_val= vals.max()
    index= vals.argmax()
    # Phản hồi
    if max_val <= 0.15:
        sorry_response= ['Xin lỗi, Tôi chưa nghe rõ câu hỏi của bạn hoặc có thể vấn đề bạn hỏi nằm ngoài sự hiểu biết của tôi.',
                          'Xin lỗi, Tôi chưa nghe rõ câu hỏi của bạn.',
                          'Xin lỗi, có thể vấn đề bạn hỏi nằm ngoài sự hiểu biết của tôi.',
                          'Bạn có thể nhắc lại câu hỏi lần nữa được không?']
        response= random.choice(sorry_response)
    else:
        response= sample_answer[index]
    
    return response

# Các mẫu chào hỏi
greeting_inputs= ('xin chào', 'chào bạn',)
greeting_responses= ['Chào bạn, rất vui được hỗ trợ cho bạn!',
                     'Xin chào, rất vui được hỗ trợ cho bạn!',
                     'Xin chào, tôi có thể cung cấp cho bạn một số thông tin về tỉnh Quảng Bình!',
                     'Chào bạn, tôi có thể cung cấp cho bạn một số thông tin về tỉnh Quảng Bình!',
                     'Xin chào, rất mong các thông tin hỗ trợ của tôi sẽ giúp ích cho bạn!',
                     'Chào bạn, rất mong các thông tin hỗ trợ của tôi sẽ giúp ích cho bạn!']

# Các mẫu nói tục
swearing_inputs= ('**', '***')
swearing_responses= ['Tôi xin phép không trả lời vì câu hỏi của bạn thiếu nghiêm túc.',
                     'Bạn có thể hỏi nghiêm túc hơn được không?']

# tạm biệt
bye_inputs= ('tạm biệt', 'xin cảm ơn', 'cảm ơn bạn','cảm ơn')
bye_responses= ['Tạm biệt!',
                'Rất vui được hỗ trợ bạn!',
                'Rất mong được gặp lại!']

# Font chữ
class font_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CBLINK = '\33[5m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    

# Thu âm
r = sr.Recognizer()
def audio_to_text(print_text= True):
    with sr.Microphone() as source:
        print(font_colors.CBLINK + '\n...' + font_colors.ENDC)
        try:
            audio = r.listen(source, timeout= 7)
            text_from_audio= r.recognize_google(audio,language='vi-VN')
        except:
            text_from_audio= '...'
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
    if print_text:
        print(font_colors.CGREEN + '\nBạn nói:', text_from_audio + font_colors.ENDC)
    return text_from_audio

# Nói của Google
def speed(text):
    print(font_colors.CRED + '\nMáy nói:', text + font_colors.ENDC)
    tts= gTTS(text, lang='vi')
    file_name= 'speed.mp3'
    tts.save(file_name)
    playsound.playsound(file_name)

def robot_brain():
    flag= True
    n_silent = 0
    while flag:
        user_response = audio_to_text()
        if  user_response == '...':
            n_silent += 1
        else:
            n_silent = 0
        if n_silent >= 3: # 3 lần im lặng tự ngắt
            flag= False
        user_response= user_response.lower()
        
        if (True in [greeting_input in user_response for greeting_input in greeting_inputs]) and (user_response.count(' ') <= 6):
            speed(random.choice(greeting_responses))
        elif (True in [swearing_input in user_response for swearing_input in swearing_inputs]):
            speed(random.choice(swearing_responses))
        elif (True in [bye_input in user_response for bye_input in bye_inputs]) and (user_response.count(' ') <= 6):
            speed(random.choice(bye_responses))
            flag= False
        else:
            speed(response(user_response))
    
begin_1= 'Tôi là tổng đài cung cấp thông tin tự động về tỉnh Quảng Bình.'
begin_2= 'Để bắt đầu hãy nói "Xin chào" và nói "Tạm biệt" để kết thúc.'
speed(begin_1)
speed(begin_2)
robot_brain()


print()
print('KÉT THÚC')