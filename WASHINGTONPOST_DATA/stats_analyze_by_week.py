import datetime as dt
import numpy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib

def f7(seq):
    #a method that remove duplicates without reordering
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def to_week_date(date):
    #this method inputs a yr, month, day and returns the date of the first day in that month
    yr=int(str(date)[0:4])
    mth=int(str(date)[4:6])
    day=int(str(date)[6:8])
    week=dt.date(yr,mth, day).isocalendar()[1]
    year=dt.date(yr,mth, day).isocalendar()[0]
    week_year = str(year) + str(week)
    return int(str(dt.datetime.strptime(week_year+ '-1',"%Y%W-%w")).split(" ")[0].replace('-',""))

def week_score(data,dates):
    #takes in a data list and the corresponding dates
    #the dates are the first day of that week
    #and then calculates the average score in that week
    score_list=[]
    week_date=f7(dates)
    for x in week_date:
        first=dates.index(x)
        last=len(dates)-dates[::-1].index(x)
        n=last-first
        total=float(0)
        for x in data[first:last]:
            total+=x
        score_list.append(total/float(n))
    return [score_list,week_date]


matplotlib.rcParams.update({'font.size': 8})
def plot_analyze(h_file,t_file,title):
    #plot all the points and the weekly analysis
    h=open(h_file,'r')
    t=open(t_file,'r')
    datas=set([])
    for line in h:
        datas.add(line)
    for line in t:
        datas.add(line)
    h_data=[]
    t_data=[]
    for x in datas:
        x_list=x.split(", ")
        if x_list[2]=='H':
            h_data.append([x_list[1],x_list[3]])
        elif x_list[2]=='T':
            t_data.append([x_list[1], x_list[3]])
    h_data=sorted(h_data,key=lambda x:x[0])
    t_data=sorted(t_data,key=lambda x:x[0])
    h_dates=[ int(x[0]) for x in h_data]
    h_week_dates=[to_week_date(x) for x in h_dates]
    h_score=[float(x[1]) for x in h_data]
    h_week_list=week_score(h_score,h_week_dates)


    t_dates = [int(x[0]) for x in t_data]
    t_week_dates = [to_week_date(x) for x in t_dates]
    t_score = [float(x[1]) for x in t_data]
    t_week_list = week_score(t_score, t_week_dates)

    h_std=numpy.std(h_score)
    t_std=numpy.std(t_score)
    h_ave=numpy.average(h_score)
    t_ave=numpy.average(t_score)
    x = [dt.datetime.strptime(str(d), "%Y%m%d").date() for d in h_week_list[1]]
    x2 = [dt.datetime.strptime(str(d), "%Y%m%d").date() for d in t_week_list[1]]
    x3 = [dt.datetime.strptime(str(d), "%Y%m%d").date() for d in h_dates]
    x4 = [dt.datetime.strptime(str(d), "%Y%m%d").date() for d in t_dates]
    h_pos_counts=len(list(filter(lambda x :x>0, h_score)))
    h_neg_counts=len(list(filter(lambda x :x<0, h_score)))
    t_pos_counts = len(list(filter(lambda x: x > 0, t_score)))
    t_neg_counts = len(list(filter(lambda x: x < 0, t_score)))
    h_ratio=float(h_neg_counts)/float(h_pos_counts)
    t_ratio=float(t_neg_counts)/float(t_pos_counts)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.plot(x, h_week_list[0],'.-',label='Hillary weekly score',color='cornflowerblue')
    plt.plot(x2, t_week_list[0],'.-',label='Trump weekly score',color='red')
    plt.plot(x3, h_score,'.',label='Hillary',color='cornflowerblue')
    plt.plot(x4, t_score,'.',label='Trump',color='red')
    plt.legend()
    plt.title(title,fontsize=15)
    plt.axhline(y=0, xmin=0, xmax=1, hold=None,color='black',linestyle='--')
    description="Standard deviation for Hillary score is: %f. Average is: %f" \
                "\nStand deviation for Trump score is: %f. Average is: %f" \
                "\nHillary's negative, positive ratio is: %f\n " \
                "Trump's negative, positive ratio is: %f"%(h_std,h_ave,t_std,t_ave,h_ratio,t_ratio)
    plt.figtext(0.5,0.045,description,fontsize=10,horizontalalignment='center',
        verticalalignment='center',color='navy')
    plt.ylim(-0.5,0.5)
    plt.show()



# plot_analyze("cnn_hillary_analyze_textblob.txt","cnn_trump_analyze_textblob.txt",'CNN-TEXTBLOB')
# plot_analyze("cnn_hillary_analyze_vader.txt","cnn_trump_analyze_vader.txt",'CNN-VADER')
# plot_analyze("nytimes_hillary_analyze_textblob.txt","nytimes_trump_analyze_textblob.txt",'NYTIMES-TEXTBLOB')
# plot_analyze("nytimes_hillary_analyze_vader.txt","nytimes_trump_analyze_vader.txt",'NYTIMES-VADER')
# plot_analyze("foxnews_hillary_analyze_textblob.txt","foxnews_trump_analyze_textblob.txt",'FOXNEWS-TEXTBLOB')
# plot_analyze("foxnews_hillary_analyze_vader.txt","foxnews_trump_analyze_vader.txt",'FOXNEWS-VADER')
# plot_analyze("nbc_hillary_analyze_textblob.txt","nbc_trump_analyze_textblob.txt",'NBC-TEXTBLOB')
# plot_analyze("nbc_hillary_analyze_vader.txt","nbc_trump_analyze_vader.txt",'NBC-VADER')
plot_analyze("nbc_hillary_analyze_textblob.txt","nbc_trump_analyze_textblob.txt",'WASHINGTONPOST-TEXTBLOB')
plot_analyze("washingtonpost_hillary_analyze_vader.txt","washingtonpost_trump_analyze_vader.txt",'WASHINGTONPOST-VADER')