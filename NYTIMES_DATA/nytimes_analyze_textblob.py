import RAKE
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
from textblob import TextBlob
sys.setdefaultencoding('utf8')
def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def analyze(path,output_path):
    #nytimes is particular hard
    #since it requires an account to log in
    url1 = 'https://myaccount.nytimes.com/auth/login/'

    page1 = requests.get(url1)
    soup = BeautifulSoup(page1.content)
    #go to the log in page
    # print soup.prettify()
    temp = soup.find('input', {"name": 'token'})
    #nytimes generates a tempory token for logging in
    token = temp['value']
    #get the value of that token value to log in
    temp = soup.find('input', {"name": 'expires'})
    #get the expires value
    expires = temp['value']
    username = 'xtang14@u.rochester.edu'
    password = 't1540706281'
    #account and password
    payload = {'userid': username, 'password': password, 'token': token, 'is_continue': 'true',
               'expires': expires}
    #the package to send to
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
            #go to that link by the specific package
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
                #get the main body of the article

                for x in temp:
                    paragraph = []
                    for y in x.contents:
                        #turn it into unicode.
                        #but first need to change the strings to utf-8 format
                        paragraph.append(unicode(y.string))
                    texts = ("".join(paragraph))

                    if texts!=" " and texts!="\n" and texts!="":
                        #the empty texts should not be considered
                        print texts
                        sentences.append(texts)
                        #append all the texts for keyword search
                        zen = TextBlob(unicode(texts))
                        #use either textblob or vader for sentiment analysis
                        print zen.sentiment
                        total_paragraph+=1
                        if zen.subjectivity>float(0):
                            #if the paragraph is not absolutely subjective, then
                            #it is objective
                            total_score+=float(zen.polarity)
                rake_object = RAKE.Rake('stop-word-list.txt')
                #a list of word to not be considered for keyword search
                keywords = rake_object.run("\n".join(sentences))
                #find the keywords for the entire article
                trump_prob = 0
                hillary_prob = 0
                for x in keywords:
                    #print x

                    if 'trump' in x[0] or 'donald' in x[0]:
                        #if a keyword has trump, then add its score
                        # print x
                        trump_prob += int(x[1])
                    if 'hillary' in x[0] or 'clinton' in x[0]:
                        #if a keyword has hillary, then add its score
                        # print x
                        hillary_prob += int(x[1])
                print url.strip("\n")
                print "Trump total ", trump_prob
                print "Hillary total ", hillary_prob
                if abs(trump_prob-hillary_prob)<=2:
                    #if the scores are not too cluse
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
# analyze('nytimes_hillary_url.txt','nytimes_hillary_analyze_textblob.txt')
import threading
thread1=threading.Thread(target=analyze,args=('nytimes_trump_url.txt','nytimes_trump_analyze_textblob.txt',))
thread2=threading.Thread(target=analyze,args=('nytimes_hillary_url.txt','nytimes_hillary_analyze_textblob.txt',))
try:
    thread1.start()
    thread2.start()
except:
    print "Error occurred"
