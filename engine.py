import urllib.request,time,_thread,urllib.parse
from PIL import Image, ImageFilter

class AnswerQuery:

    def __init__(self,question,answers):
        self.question=question['query_value']
        self.coefficent=question['coeff']
        self.answers=answers
        self.tread_stamp=[]

    def query_count_thread(self,url):
        self.get_answer_count(self.get_query_result(url))
        self.tread_stamp.append(time.time())

    def get_query_result(self,url):
        headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        queryResult = opener.open(url).read()

        if 'baidu.com' in url:
            queryResult=queryResult.decode('gbk').encode('utf-8').decode('utf-8')
        else:
            queryResult=str(queryResult,'utf-8')
        return queryResult

    def get_answer_count(self,result):
        for answer in self.answers:
            answer['count']+=result.count(answer['value'])*self.coefficent

    def create_thread(self,url):
        try:
            _thread.start_new_thread(self.query_count_thread,(url,))
        except:
            print('Error: unable to start thread')

    def search(self):
        sources={}
        sources['baidu']='https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word='+urllib.parse.quote(self.question,encoding='gbk')
        sources['sogou']='http://wenwen.sogou.com/s/?w='+urllib.parse.quote(self.question)+'&ch=ww.header.ssda'
        sources['sina']='https://iask.sina.com.cn/search?searchWord='+urllib.parse.quote(self.question)+'&record=1'
        sources['so']='https://wenda.so.com/search/?q='+urllib.parse.quote(self.question)

        for source in list(sources.values()):
            self.create_thread(source)
        while True:
            if len(self.tread_stamp)==len(list(sources.values())):
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
