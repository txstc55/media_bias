from bs4 import BeautifulSoup
import requests
import RAKE
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


def toTime(time_list):
    month={"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04","May":"05", "Jun":"06", "Jul":"07", "Aug":"08", "Sep":"09", "Oct":"10", "Nov":"11","Dec":"12"}
    day=""
    if len(time_list[1])==1:
        day="".join(["0",time_list[1]])
    else:
        day=time_list[1]
    month_number=month[time_list[0]]
    time_num="".join([time_list[2],month_number,day])
    return time_num

#
# url='http://www.nbcnews.com/politics/politics-news/hillary-clinton-s-popular-vote-lead-now-over-two-million-n687701'
# page = requests.get(url)
# soup = BeautifulSoup(page.content)
# print(soup.prettify())
# temp=soup.find_all("p")
# temp2=soup.find_all('p',{ "dir" : "ltr" })
# by_line=soup.find_all('p',{'class':'byline_article'})
# author=soup.find_all('p',{'class':'byline_author'})
# date=soup.find('time').text.split(',')[0].split(" ")
# print date
# for x in temp:
#     if x not in temp2 and x not in by_line and x not in author:
#         if x.text.split(":")[0]!=" Related":
#
#             print x.text
#             #print x.text.split(":")
#         #print len(x.text)
#
#
#
# print toTime(date)




def analyze(path,output_path):

    k=open(path,'r')
    o=open(output_path,'w')
    for url in k:
        if url.strip("\n").strip("\r")!="http://www.nbcnews.com/politics/2016-election":


            split_lines = url.strip("\n").strip("\r").split('/')
            if "video" not in split_lines and "id" not in split_lines and "_news" not in split_lines and "meet-the-press" not in split_lines and "www.nbcnews.com" in split_lines:
                page = requests.get(url.strip("\n").strip("\r"))
                print url.strip("\n")
                soup = BeautifulSoup(page.content)
                #print soup.prettify()
                result = []

                result.append(url.strip('\n').strip("\r"))
                print soup.find("time")
                date = toTime(soup.find('time').text.split(',')[0].split(" "))
                if int(date)>=20150101:
                    total_paragraph = 0
                    #print "over date"
                    result.append(date)
                    sentences = []
                    total_score=0
                    temp = soup.find_all("p")
                    temp2 = soup.find_all('p', {"dir": "ltr"})
                    by_line = soup.find_all('p', {'class': 'byline_article'})
                    author = soup.find_all('p', {'class': 'byline_author'})
                    for x in temp:
                        if x not in temp2 and x not in by_line and x not in author:
                            if x.text.split(":")[0] != " Related":
                                texts=x.text


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

#analyze('nbc_trump_url.txt','nbc_trump_analyze.txt')

import threading
thread1=threading.Thread(target=analyze,args=('nbc_trump_url.txt','cnn_trump_analyze_vader.txt',))
thread2=threading.Thread(target=analyze,args=('nbc_hillary_url.txt','cnn_hillary_analyze_vader.txt',))
try:
    thread1.start()
    thread2.start()
except:
    print "Error occurred"