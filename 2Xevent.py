import urllib.request
import re
import time
import datetime
import sys
from datetime import datetime, timedelta

# assumptions (if any of these are false behavior is undefined)

# news page will always have a 2x article
# event page url contains the dates of the event (ex. 12-10-12-11) which are listed in pairs
# daylight savings time does not exist (see below)
# format of times is always ##:## AM or ##:## PM
# times are always listed in pairs where the first is a start time and the second is an end time
# 2x events take place in the current year (this code won't work if it's dec 31 and there's an event on jan 1)

timedict = {}
timedict['12:00AM'] = 0
timedict['1:00AM'] = 1
timedict['2:00AM'] = 2
timedict['3:00AM'] = 3
timedict['4:00AM'] = 4
timedict['5:00AM'] = 5
timedict['6:00AM'] = 6
timedict['7:00AM'] = 7
timedict['8:00AM'] = 8
timedict['9:00AM'] = 9
timedict['10:00AM'] = 10
timedict['11:00AM'] = 11
timedict['12:00PM'] = 12
timedict['1:00PM'] = 13
timedict['2:00PM'] = 14
timedict['3:00PM'] = 15
timedict['4:00PM'] = 16
timedict['5:00PM'] = 17
timedict['6:00PM'] = 18
timedict['7:00PM'] = 19
timedict['8:00PM'] = 20
timedict['9:00PM'] = 21
timedict['10:00PM'] = 22
timedict['11:00PM'] = 23

add_hours_for_testing = 0

# will need to be changed to -7 during daylight savings
# or look into "pytz" module for more accurate pst/pdt calculation
pst_timedifference = -8

currentyear = datetime.utcnow().year
currenttimepst = datetime.utcnow() + timedelta(hours=pst_timedifference) + timedelta(hours=add_hours_for_testing)

mainPage = ("http://maplestory.nexon.net/news")
try:
    htmltext = urllib.request.urlopen(mainPage).read().decode('utf-8')
    regex = '<a href="/news/(.+?)/2x-exp-drop-event-(.+?)">' #Gets the link with the event page
    linkPart = re.findall(re.compile(regex),htmltext)[0]
except:
    print ("The next 2x event is not yet announced in a supported format.")
    sys.exit()
eventpageid = linkPart[0]
monthsanddays = re.findall(re.compile('[0-9]{1,2}'),linkPart[1])

eventPage = "http://maplestory.nexon.net/news/" + eventpageid
try:
    htmltext = urllib.request.urlopen(eventPage).read().decode('utf-8')
    regex = '<strong>PST:(.+?)</strong>' #Gets the link with the event data
    timeList = re.findall(re.compile(regex),htmltext)
    
    startTimes = []
    endTimes = []
    
    for i, t in enumerate(timeList):
        temp = re.sub(' ', '', t)
        newList = re.findall(re.compile("[0-9]{1,2}:[0-9]{2}[AP]M"),temp)
    
        for j, n in enumerate(newList):
            eventdatetime = datetime(currentyear, int(monthsanddays[0]), int(monthsanddays[1])).replace(hour=timedict[n])
            
            if eventdatetime - currenttimepst > timedelta(seconds=0):
                if j % 2 == 0:
                    startTimes.append(eventdatetime)
                    #print(eventdatetime - currenttimepst)
                else :
                    endTimes.append(eventdatetime)
    
        monthsanddays.pop(0)
        monthsanddays.pop(0)
    
    #print(currenttimepst, startTimes)
    
    if len(endTimes) > 0:
        nextEndtime = endTimes[0]
        if len(startTimes) == 0 or startTimes[0] - nextEndtime > timedelta(seconds=0):
            timeSpan = nextEndtime.replace(microsecond=0) - currenttimepst.replace(microsecond=0)
            print("The currently running 2x event ends at " + nextEndtime.strftime("%b %d %Y %H:%M:%S") + " PST (in " + str(timeSpan) + ")")
    
    if len(startTimes) > 0:
        nextStartTime = startTimes[0]
    
        timeSpan = nextStartTime.replace(microsecond=0) - currenttimepst.replace(microsecond=0)
        print("The next 2x event starts at " + nextStartTime.strftime("%b %d %Y %H:%M:%S") + " PST (in " + str(timeSpan) + ")")
except:
    print ("Either nexon is inconsistent at announcing their 2x exp events, or this plugin is coded by monkeys. We don't know.")
