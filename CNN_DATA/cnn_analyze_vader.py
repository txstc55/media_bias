import RAKE
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# url='http://www.cnn.com/2016/09/11/politics/hillary-clinton-health-2016-election/'
# page = requests.get(url)
# soup = BeautifulSoup(page.content)
# #print(soup.prettify())
#
# #print soup.find('div',{'class': 'el__leafmedia el__leafmedia--sourced-paragraph'}).text
# temp=soup.find_all("div",{ "class" : "zn-body__paragraph" })
# split_lines = url.split('/')
# date="".join(split_lines[3:6])
# for x in temp:
#     print x.text
#
# print date

def analyze(path,output_path):

    k=open(path,'r')
    o=open(output_path,'w')
    for url in k:
        print url
        split_lines = url.split('/')
        if RepresentsInt(split_lines[3]) and RepresentsInt(split_lines[4]) and RepresentsInt(split_lines[5]):


            #request_page=['https://myaccount.nytimes.com/auth/login/?URI=',url]
            #print "".join(request_page)
            #page = requests.get(url)
            #soup = BeautifulSoup(page.content)
            result = []
            result.append(url.strip('\n'))
            date = "".join(split_lines[3:6])
            #print date
            if int(date)>=20150101:
                total_paragraph = 0
                #print "over date"
                result.append(date)
                sentences = []
                page = requests.get(url.strip("\n"))


                soup = BeautifulSoup(page.content)
                #neg = 0.0
                #neu = 0.0
                #pos = 0.0
                total_score=0
                header=soup.findAll('div',{'class': 'el__leafmedia el__leafmedia--sourced-paragraph'})
                for x in header:
                    if x.text != " " and x.text != "\n" and x.text != "":
                        print x.text
                        sentences.append(x.text)
                        zen = vaderSentiment(unicode(x.text))
                        print zen
                        total_paragraph += 1
                        if zen['neu'] < float(1):
                            if zen['pos'] > zen['neg']:
                                total_score += zen['pos']
                            else:
                                total_score -= zen['neg']
                temp = soup.find_all("div", {"class": "zn-body__paragraph"})
                for x in temp:
                    paragraph = []
                    for y in x.contents:
                        paragraph.append(unicode(y.string))
                    # data = ("".join(paragraph))
                    texts = ("".join(paragraph))

                    if texts != " " and texts != "\n" and texts != "":
                        print texts
                        sentences.append(texts)
                        zen = vaderSentiment(unicode(texts))
                        print zen
                        total_paragraph += 1
                        if zen['neu'] < float(1):
                            if zen['pos'] > zen['neg']:
                                total_score += zen['pos']
                            else:
                                total_score -= zen['neg']
                rake_object = RAKE.Rake('stop-word-list.txt')
                keywords = rake_object.run("\n".join(sentences))
                trump_prob = 0
                hillary_prob = 0
                for x in keywords:
                    # print x

                    if 'trump' in x[0] or 'donald' in x[0]:
                        # print x
                        trump_prob += int(x[1])
                    if 'hillary' in x[0] or 'clinton' in x[0]:
                        # print x
                        hillary_prob += int(x[1])
                print url.strip("\n")
                print "Trump total ", trump_prob
                print "Hillary total ", hillary_prob
                if abs(trump_prob - hillary_prob) <= 2:
                    result.append("B")
                elif trump_prob > hillary_prob:
                    result.append("T")
                else:
                    result.append("H")
                # zen=vaderSentiment("\n".join(sentences))
                # if zen['neu']<0.5:
                #     if zen['pos']>zen['neg']:
                #         total_score=zen['pos']
                #     else:
                #         total_score=zen['neg']
                # total = neg + neu + pos
                # if total!=0:

                if total_paragraph != 0:
                    print "Total: ", total_score / total_paragraph
                    print "Total paragraph: ", total_paragraph
                    # print "Neg: ", neg
                    # print "Neu: ", neu
                    # print "Pos: ", pos
                    print "\n"
                    # result.append(str(neg))
                    # result.append(str(neu))
                    # result.append(str(pos))
                    result.append(str(total_score / total_paragraph))
                    # print result
                    o.writelines(", ".join(result) + "\n")

#analyze('cnn_hillary_url.txt','cnn_hillary_analyze.txt')

import threading
thread1=threading.Thread(target=analyze,args=('cnn_trump_url.txt','cnn_trump_analyze_vader.txt',))
thread2=threading.Thread(target=analyze,args=('cnn_hillary_url.txt','cnn_hillary_analyze_vader.txt',))
try:
    thread1.start()
    thread2.start()
except:
    print "Error occurred"