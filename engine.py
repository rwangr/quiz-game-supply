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

import urllib.request,time,_thread,urllib.parse,traceback
from PIL import Image, ImageFilter

class AnswerQuery:

    def __init__(self,question,answers):
        self.question=question['query_value']
        self.coefficent=question['coeff']
        self.answers=answers
        self.sources={}
        self.sources['baidu']='https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word='+urllib.parse.quote(self.question,encoding='gbk')
        self.sources['sogou']='http://wenwen.sogou.com/s/?w='+urllib.parse.quote(self.question)+'&ch=ww.header.ssda'
        self.sources['sina']='https://iask.sina.com.cn/search?searchWord='+urllib.parse.quote(self.question)+'&record=1'
        self.sources['so']='https://wenda.so.com/search/?q='+urllib.parse.quote(self.question)
        self.treadStamp=[]
        self.startTime=time.time()
        self.timeout=6

    def query_count_thread(self,url):
        self.get_answer_count(self.get_query_result(url))
        self.treadStamp.append(time.time())

    def get_query_result(self,url):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Linux) AppleWebKit/604.4.7 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/604.4.7')]

        try:
            queryResult = opener.open(url).read()
            if '=gbk' in url:
                queryResult=queryResult.decode('gbk').encode('utf-8').decode('utf-8')
            else:
                queryResult=str(queryResult,'utf-8')
        except Exception as e:
            _thread.exit()

        return queryResult

    def get_answer_count(self,result):
        try:
            for answer in self.answers:
                answer['count']+=result.count(answer['value'])*self.coefficent
        except Exception as e:
            _thread.exit()

    def create_thread(self,url):
        try:
            return _thread.start_new_thread(self.query_count_thread,(url,))
        except Exception as e:
            print ('Unexpected error: Unable to start the thread')

    def search(self):
        for source in list(self.sources.values()):
            self.create_thread(source)

        while True:
            if len(self.treadStamp)==len(list(self.sources.values())) or time.time()-self.startTime>self.timeout:
                break

        return self.answers


class AreaBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=20, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)
