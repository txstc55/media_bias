import RAKE
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
sys.setdefaultencoding('utf8')
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def analyze(path,output_path):
    url1 = 'https://myaccount.nytimes.com/auth/login/'
    page1 = requests.get(url1)
    soup = BeautifulSoup(page1.content)
    # print soup.prettify()
    temp = soup.find('input', {"name": 'token'})
    token = temp['value']
    temp = soup.find('input', {"name": 'expires'})
    expires = temp['value']
    username = 'xtang14@u.rochester.edu'
    password = 't1540706281'

    payload = {'userid': username, 'password': password, 'token': token, 'is_continue': 'true',
               'expires': expires}
    s = requests.session()
    k=open(path,'r')
    o=open(output_path,'w')
    for url in k:
        #print url
        split_lines = url.split('/')
        if RepresentsInt(split_lines[3]):


            #request_page=['https://myaccount.nytimes.com/auth/login/?URI=',url]
            #print "".join(request_page)
            page = s.post(
                'https://myaccount.nytimes.com/auth/login/?URI='+url,
                data=payload)
            result=[]
            result.append(url.strip('\n').strip("\r"))
            date="".join(split_lines[3:6])
            if int(date)>=20150101:
                result.append(date)
                sentences = []
                soup = BeautifulSoup(page.content)
                total_score=0
                total_paragraph=0
                temp = soup.find_all("p", {"class": "story-body-text story-content"})
                for x in temp:
                    paragraph = []
                    for y in x.contents:
                        paragraph.append(unicode(y.string))
                    #data = ("".join(paragraph))
                    texts = ("".join(paragraph))

                    if texts!=" " and texts!="\n" and texts!="":
                        print texts
                        sentences.append(texts)
                        zen = vaderSentiment(unicode(texts))
                        print zen
                        total_paragraph+=1
                        if zen['neu']<float(1):
                            if zen['pos']>zen['neg']:
                                total_score+=zen['pos']
                            else:
                                total_score-=zen['neg']
                rake_object = RAKE.Rake('stop-word-list.txt')
                keywords = rake_object.run("\n".join(sentences))
                trump_prob = 0
                hillary_prob = 0
                for x in keywords:
                    #print x

                    if 'trump' in x[0] or 'donald' in x[0]:
                        # print x
                        trump_prob += int(x[1])
                    if 'hillary' in x[0] or 'clinton' in x[0]:
                        # print x
                        hillary_prob += int(x[1])
                print url.strip("\n")
                print "Trump total ", trump_prob
                print "Hillary total ", hillary_prob
                if abs(trump_prob-hillary_prob)<=2:
                    result.append("B")
                elif trump_prob>hillary_prob:
                    result.append("T")
                else:
                    result.append("H")
                #zen=vaderSentiment("\n".join(sentences))
                # if zen['neu']<0.5:
                #     if zen['pos']>zen['neg']:
                #         total_score=zen['pos']
                #     else:
                #         total_score=zen['neg']
                #total = neg + neu + pos
                #if total!=0:

                if total_paragraph!=0:

                    print "Total: ",total_score/total_paragraph
                    print "Total paragraph: ", total_paragraph
                    # print "Neg: ", neg
                    # print "Neu: ", neu
                    # print "Pos: ", pos
                    print "\n"
                    # result.append(str(neg))
                    # result.append(str(neu))
                    # result.append(str(pos))
                    result.append(str(total_score/total_paragraph))
                    #print result
                    o.writelines(", ".join(result)+"\n")

#
#analyze('nytimes_trump_url.txt','nytimes_trump_analyze.txt')
#
# analyze('nytimes_hillary_url.txt','nytimes_hillary_analyze.txt')
import threading
thread1=threading.Thread(target=analyze,args=('nytimes_trump_url.txt','nytimes_trump_analyze_vader.txt',))
thread2=threading.Thread(target=analyze,args=('nytimes_hillary_url.txt','nytimes_hillary_analyze_vader.txt',))
try:
    thread1.start()
    thread2.start()
except:
    print "Error occurred"
