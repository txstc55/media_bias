# from bs4 import BeautifulSoup
# import requests
# url='http://www.foxnews.com/entertainment/2016/11/22/kanye-west-reportedly-hospitalized-after-abruptly-canceling-remaining-leg-saint-pablo-tour.html'
# page = requests.get(url)
# soup = BeautifulSoup(page.content)
# print(soup.prettify())
# temp=soup.find_all('div', {"class": "article-text"})
# for x in temp:
#     for y in x.contents:
#         temp=unicode(y.string).strip('\n')
#         if temp!=""  and temp!='None':
#             print temp


import RAKE
from bs4 import BeautifulSoup
import requests
import sys
import time
from textblob import TextBlob
reload(sys)
sys.setdefaultencoding('utf8')


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def extract_time_fox_news(link):
    #a method to extract the time if it does not happen in a specific place
    #if three consecutive numbers are found, then extract them
    #those three numbers will probably be the date
    #no exception considered
    temp=link.strip('\n').strip('\r').split("/")
    for x in range(0,len(temp)):
        if x+2<=len(temp)-1 and RepresentsInt(temp[x]) and RepresentsInt(temp[x+1]) and RepresentsInt(temp[x+2]):
            year=temp[x]
            month= temp[x+1]
            day= temp[x+2]
            return int("".join([year,month,day]))
    return 0


def analyze(path,output_path):

    k=open(path,'r')
    o=open(output_path,'w')
    for url in k:
        print url
        split_lines = url.split('/')
        date=extract_time_fox_news(url)
        if date!=0:
            result = []
            result.append(url.strip('\n').strip('\r'))
            if date>=20150101 and 'v' not in split_lines:
                total_paragraph = 0
                print date
                result.append(str(date))
                sentences = []
                page = requests.get(url.strip("\n"))


                soup = BeautifulSoup(page.content)
                total_score=0
                temp = soup.find_all('div', {"class": "article-text"})
                for x in temp:
                    for y in x.contents:
                        texts=unicode(y.string).strip('\n')

                        if texts != " " and texts != "\n" and texts != "" and texts!="\r" and not "This material may not be published, broadcast, rewritten, or redistributed." in texts and texts!='None':
                            print texts
                            sentences.append(texts)
                            zen = TextBlob(unicode(texts))
                            print zen.sentiment
                            total_paragraph += 1
                            if zen.subjectivity > float(0):
                                total_score += float(zen.polarity)
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

analyze('foxnews_trump_url.txt','foxnews_trump_analyze_textblob.txt')
analyze('foxnews_hillary_url.txt','foxnews_hillary_analyze_textblob.txt')
# import threading
# thread1=threading.Thread(target=analyze,args=('cnn_trump_url.txt','cnn_trump_analyze.txt',))
# thread2=threading.Thread(target=analyze,args=('cnn_hillary_url.txt','cnn_hillary_analyze.txt',))
# try:
#     thread1.start()
#     thread2.start()
# except:
#    print "Error occurred"