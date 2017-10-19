# import datetime
# week= datetime.date(2016,01, 03).isocalendar()[1]
# year= datetime.date(2016,01, 03).isocalendar()[0]
#
# print year
# print week
# week_year=str(year)+str(week)
# print week_year
# print str(datetime.datetime.strptime(week_year+ '-1',"%Y%W-%w")).split(" ")[0].replace('-',"")

#
# def f7(seq):
#     seen = set()
#     seen_add = seen.add
#     return [x for x in seq if not (x in seen or seen_add(x))]
text="'Cendrillon', dat was nu nog eens genieten. #munt #sprookje #wateenkostuums'"
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
vad=vaderSentiment(text)
print vad
from textblob import TextBlob
print TextBlob("This is evil").sentiment