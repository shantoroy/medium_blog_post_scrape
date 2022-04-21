import pandas as pd
import csv
import time
import numpy as np
from matplotlib import pyplot as plt
from numpy import int32
from datetime import datetime


from numpy import int32
from datetime import datetime
import operator

data_sheet_Questions = pd.read_json('final_data_removing_duplicacy.json', encoding='latin-1')



Question_count = data_sheet_Questions.shape[0]

print("No of Questions in StackOverflow = "+format(Question_count))
#print(data_sheet_Questions.CreationDate)
# print(data_sheet.dtypes)
data_sheet_Questions['publish_date'] = pd.to_datetime(data_sheet_Questions['publish_date'])
print(data_sheet_Questions.publish_date)

count19 = 0
count18 = 0
count17 = 0
count16 = 0
count15 = 0
count14 = 0

#l = data_sheet.sort_values(by='CreationDate')

month2019 = [0] * 13
month2018 = [0] * 13
month2017 = [0] * 13
month2016 = [0] * 13
month2015 = [0] * 13
month2014 = [0] * 13


for k in data_sheet_Questions.publish_date:
    date, time = str(k).split(" ")  # Date and time splitting

    # date parsing
    y, m, d = date.split("-")
    if y == "2019":
        m = int(m)
        month2019[m] += 1
        count19 += 1

    elif y == "2018":
        m = int(m)
        month2018[m] += 1
        count18 += 1


    elif y == "2017":
        m = int(m)
        month2017[m] += 1
        count17 += 1

    elif y == "2016":
        m = int(m)
        month2016[m] += 1
        count16 += 1

    elif y == "2015":
        m = int(m)
        month2015[m] += 1
        count15 += 1

    elif y == "2014":
        m = int(m)
        month2014[m] += 1
        count14 += 1


f= open("No_of_Questions_PerMonthPerYear.txt","w+")
f.write("\t\t\t\t2019")
f.write("\n\nNumber of total Questions in 2019 is = {}\n\n".format(count19))
#Only for month of 2019
f.write(" Month    No of Questions")     #table column headings
f.write("\n------ \t -------------")
for i in range(1,len(month2019)):
    f.write("\n{} \t\t\t\t {}".format(i,month2019[i]))

f.write("\n\n\n\t\t\t\t2018")
f.write("\n\nNumber of total Questions in 2018 is = {}\n\n".format(count18))
#Only for month of 2018
f.write(" Month    No of Questions")     #table column headings
f.write("\n------ \t -------------")
for i in range(1,len(month2018)):
    f.write("\n{} \t\t\t\t {}".format(i,month2018[i]))

f.write("\n\n\n\t\t\t\t2017")
f.write("\n\nNumber of total Questions in 2017 is = {}\n\n".format(count17))
# Only for month of 2017
f.write(" Month    No of Questions")  # table column headings
f.write("\n------ \t -------------")
for i in range(1, len(month2017)):
    f.write("\n{} \t\t\t\t {}".format(i, month2017[i]))


f.write("\n\n\n\t\t\t\t2016")
f.write("\n\nNumber of total Questions in 2016 is = {}\n\n".format(count16))
# Only for month of 2016
f.write(" Month    No of Questions")  # table column headings
f.write("\n------ \t -------------")
for i in range(1, len(month2016)):
    f.write("\n{} \t\t\t\t {}".format(i, month2016[i]))


f.write("\n\n\n\t\t\t\t2015")
f.write("\n\nNumber of total Questions in 2015 is = {}\n\n".format(count15))
# Only for month of 2015
f.write(" Month    No of Questions")  # table column headings
f.write("\n------ \t -------------")
for i in range(1, len(month2015)):
    f.write("\n{} \t\t\t\t {}".format(i, month2015[i]))


f.write("\n\n\n\t\t\t\t2014")
f.write("\n\nNumber of total Questions in 2014 is = {}\n\n".format(count14))
# Only for month of 2014
f.write(" Month    No of Questions")  # table column headings
f.write("\n------ \t -------------")
for i in range(1, len(month2014)):
    f.write("\n{} \t\t\t\t {}".format(i, month2014[i]))

f.close()



years=['2014', '2015', '2016', '2017', '2018', '2019']
y_pos=np.arange(len(years))
plt.bar(y_pos,[count14,count15,count16,count17,count18,count19])
plt.xticks(y_pos, years)

plt.ylabel('No of Questions')
plt.title("Questions from May 14 - January 19")
plt.show()



months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
y_pos=np.arange(len(months))

plt.gca()
plt.plot(months,month2019[1:])
plt.plot(month2018[1:])
plt.plot(month2017[1:])
plt.plot(month2016[1:])
plt.plot(month2015[1:])
plt.plot(month2014[1:])
plt.title("Questions on Smart Contracts Over Years")
plt.legend(['Monthly Questions for 2019', 'Monthly Questions for 2018', 'Monthly Questions for 2017', 'Monthly Questions for 2016', 'Monthly Questions for 2015', 'Monthly Questions for 2014'], loc='upper right')
plt.show()


f = plt.figure()
ax=f.add_subplot(231)
ax.set_ylim([0, 300])
plt.bar(y_pos, month2019[1:])
plt.xticks(y_pos, months)
plt.ylabel('No of Questions in 2019')
plt.title("No of Monthly Questions of 2019")

ax=f.add_subplot(232)
ax.set_ylim([0, 300])
plt.bar(y_pos, month2018[1:])
plt.xticks(y_pos, months)
plt.ylabel('No of Questions in 2018')
plt.title("No of Monthly Questions of 2018")

ax=f.add_subplot(233)
ax.set_ylim([0, 300])
plt.bar(y_pos, month2017[1:])
plt.xticks(y_pos, months)
plt.ylabel('No of Questions in 2017')
plt.title("No of Monthly Questions of 2017")

ax=f.add_subplot(234)
ax.set_ylim([0, 300])
plt.bar(y_pos, month2016[1:])
plt.xticks(y_pos, months)
plt.ylabel('No of Questions in 2016')
plt.title("No of Monthly Questions of 2016")

ax=f.add_subplot(235)
ax.set_ylim([0, 300])
plt.bar(y_pos, month2015[1:])
plt.xticks(y_pos, months)
plt.ylabel('No of Questions in 2015')
plt.title("No of Monthly Questions of 2015")

ax=f.add_subplot(236)
ax.set_ylim([0, 300])
plt.bar(y_pos, month2014[1:])
plt.xticks(y_pos, months)
plt.ylabel('No of Questions in 2014')
plt.title("No of Monthly Questions of 2014")

plt.show()
# the x locations for the groups
# ax = plt.subplot(111)




width = 0.20
Months=['January','February','March','April','May','June','July','August','September','October','November','December']
fig = plt.figure()
ax = fig.add_subplot(111)
#for i in range(len(month2018)):
Q2019 = ax.bar(y_pos, month2019[1:], width, color='red')
Q2018 = ax.bar(y_pos+width, month2018[1:], width, color='green')
Q2017 = ax.bar(y_pos+width*2, month2017[1:], width, color='blue')
Q2016 = ax.bar(y_pos+width*3, month2016[1:], width, color='orange')
Q2015 = ax.bar(y_pos+width*4, month2015[1:], width, color='purple')
Q2014 = ax.bar(y_pos+width*5, month2014[1:], width, color='black')
ax.legend( ([Q2019, Q2018, Q2017, Q2016, Q2015, Q2014]), ('2019', '2018', '2017','2016', '2015', '2014') )
ax.set_ylabel('No of Questions')
ax.set_xticks(y_pos+width)
ax.set_xticklabels(Months)
plt.show()


# My code starts from here
y_pos = np.arange(72)
years = ["2014", "2015", "2016", "2017", "2018", "2019"]
f = plt.figure()
ax.set_ylim([0, 300])
plt.bar(y_pos, month2014[1:]+month2015[1:]+month2016[1:]+month2017[1:]+month2018[1:]+month2019[1:])
# width = 0.25
plt.xticks(range(1,72,12), years)
plt.ylabel('No of Posts')
plt.title("Number of posts over the time")
plt.show()