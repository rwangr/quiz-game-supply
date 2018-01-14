'''
MIT License

Copyright (c) 2018 Ryan Wang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import urllib.request,sys,base64,json,os,time,string,re,os,string
from configparser import ConfigParser
from PIL import Image
from aip import AipOcr
from zhon import hanzi
from engine import AnswerQuery,AreaBlur

# Parameter
QUIZ_APPS=[
{'app_name':'冲顶大会',
 'answer_count':3,
 'crop_area':(45,190,450,580), #iPhone 6,6s,7 on 1440*900 display resolution Mac
 'mask_area':[]},

{'app_name':'芝士超人',
 'answer_count':3,
 'crop_area':(24,120,470,500), #iPhone 6,6s,7 on 1440*900 display resolution Mac
 'mask_area':[]},

{'app_name':'头脑王者',
 'answer_count':4,
 'crop_area':(65,250,430,810), #iPhone 6,6s,7 on 1440*900 display resolution Mac
 'mask_area':[(25,435,85,465),(410,435,470,465)]}, #iPhone 6,6s,7 on 1440*900 display resolution Mac

 {'app_name':'头脑王者(iPhone X)',
  'answer_count':4,
  'crop_area':(50,250,350,825), #iPhone X on 1440*900 display resolution Mac
  'mask_area':[(20,520,70,540),(340,520,390,540)]} #iPhone X on 1440*900 display resolution Mac
]

NEG_KEYWORDS=['不','没']

# Configuration
cfg = ConfigParser()
cfg.read('secret.ini')
client = AipOcr(cfg.get('BAIDU_OCR','APP_ID'), cfg.get('BAIDU_OCR','API_KEY'), cfg.get('BAIDU_OCR','SECRET_KEY'))

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def is_contain_keywords(text,keywords):
    for word in keywords:
        if text.count(word)>0:
            return True
    return False

def clear_keywords(text,keywords):
    for word in keywords:
        text=text.replace(word,'')
    return text

# Select quiz app
print('---------------------------------')
print('The supported quiz app are as below:')
for appSeq in range(len(QUIZ_APPS)):
    print(appSeq+1, QUIZ_APPS[appSeq]['app_name'])
selectedSeq=input(r'Press No. to select your app. Press other key to exit: ')
try:
    selectedSeq=int(selectedSeq)-1
    if not selectedSeq in range(len(QUIZ_APPS)):
        raise ValueError()
except:
    exit()
print('[',QUIZ_APPS[selectedSeq]['app_name'],']','has been selected')

while True:
    nextStep=input('Press [Enter] to pick answer. Press other key to exit: ')
    if nextStep=='':
        startTime = time.time()

        # Capture, crop image, and mask noise
        fullCapFileName=r'./sreenshot/full_'+str(int(startTime))+'.png'
        subjectCapFileName=r'./sreenshot/subject_'+str(int(startTime))+'.png'
        os.system('screencapture '+fullCapFileName)
        fullCap=Image.open(fullCapFileName)
        if len(QUIZ_APPS[selectedSeq]['mask_area'])>0:
            for area in QUIZ_APPS[selectedSeq]['mask_area']:
                fullCap=fullCap.filter(AreaBlur(bounds=area))
        fullCap.crop(QUIZ_APPS[selectedSeq]['crop_area']).save(subjectCapFileName)

        # Read cropped image
        image = get_file_content(subjectCapFileName)
        response = client.basicGeneral(image)
        wordsResult=response['words_result']
        #print(wordsResult)
        #wordsResult=[{'words': '下列哪个岛国不是欧洲国家?'}, {'words': '爱尔兰'}, {'words': '马尔代夫'}, {'words': '马耳他'}]

        # Store recognized text in dict
        answerCount=QUIZ_APPS[selectedSeq]['answer_count']
        subject={}
        subject['question']={'value':''.join([seg['words'] for seg in wordsResult[0:len(wordsResult)-answerCount]])}
        if is_contain_keywords(subject['question']['value'],NEG_KEYWORDS):
            subject['question']['coeff']=-1
            subject['question']['query_value']=clear_keywords(subject['question']['value'],NEG_KEYWORDS)
        else:
            subject['question']['coeff']=1
            subject['question']['query_value']=subject['question']['value']
        subject['answers']=[{'value':seg['words'].strip(string.punctuation).strip(hanzi.punctuation),'count':0} for seg in wordsResult[len(wordsResult)-answerCount:]]

        # Query question and obtain each of answer frequency
        query=AnswerQuery(subject['question'],subject['answers'])
        subject['answers']=query.search()

        # Print the result
        print('---------------------------------')
        print(subject['question']['value'])
        for answer in subject['answers']:
            print (('>>' if answer['count']== max([answer['count'] for answer in subject['answers']]) else '  '),answer['value'],'[',answer['count'],']')
        print('---------------------------------')
        print('time cost: '+str(time.time()-startTime)+'s')
    else:
        exit()
