#### CALENDARS DONE ####
    # 9M11
    # 9U11
    # 9W11
    # 9H11
    # 9F11

    # 9M21
    # 9U11
    # 9W11
    # 9H11
    # 9F11


 #### IMPORTS #####

import time
from datetime import date, timedelta, time, datetime
import numpy
from AllThingsClickCopy import GetClickObject, UpdateClickObject
from AllThingsClickCopy import prodObjectCheck
from AllThingsClickCopy import environmentUsr
from AllThingsClickCopy import environmentPwd
## VARIABLE ##


###  VARIABLES ###
prodCheck = False
env = 'DEV'
params = ''
clickObj = 'Calendar'

### FUNCTIONS ####

# Function to calculate startDate intervals -> startDate start and startDate end times
def automate_time(start_hour, start_minute, startDate, name):
    time_str = startDate.strftime("%H::%M::%S")  # extracting time from the startDate object into startTimestring
    time_object = datetime.strptime(time_str, '%H::%M::%S')# converting time_str into datetime object
    startTime= time(start_hour, start_minute)  #startDate start time
    
    #Calculating startDate end time
    if (name == "9F11" or name == "9F21"):
        b = time_object+timedelta(days=+0, hours=+8, minutes=+30)
    else:
        b = time_object+timedelta(days=+0, hours=+9, minutes=+30)

    endTime = datetime.strptime(str(b), "%Y-%m-%d %H:%M:%S").time()
    print("Start Time: ",startTime)
    print("End Time: ", endTime)
    #print("End Time: ",datetime.strptime(str(b), "%Y-%m-%d %H:%M:%S").time())
    
    #if condition to schedule short-Friday-startDates for alternating Mon,Tues,Wed,Thurs
    #It exlcudes calendars 9F11 and 9F21
    if (name == "9M11" or name == "9M21" or  name == "9U11" or name == "9U21" or name == "9W11" or name == "9W21" or name == "9H11" or name == "9H21"):
        #initializing next_day and next_startDate variables
        next_day = timedelta(days=+0)
        next_startDate = startDate + next_day
        
        #if conditions to make sure that calendar name and dates match
        if ((name == "9M11" or name == "9M21") and (startDate.strftime("%A")=="Monday")):
            next_day = timedelta(days=+4)
        if ((name == "9U11" or name == "9U21") and (startDate.strftime("%A")=="Tuesday")):
            next_day = timedelta(days=+3)
        if ((name == "9W11" or name == "9W21")and (startDate.strftime("%A")=="Wednesday")):
            next_day = timedelta(days=+2)
        if ((name == "9H11" or name == "9H21") and (startDate.strftime("%A")=="Thursday")):
             next_day = timedelta(days=+1)
        
        next_startDate = startDate + next_day
        print("Next Start Date:", next_startDate.strftime("%Y-%m-%d")) ## Friday
        day = next_startDate.strftime("%A")
        print("Day: ",day )    
        a1 = time(start_hour+1, start_minute, 00) ##new start time for Friday
        print("Start Time: ", a1)
        print("End Time: ",endTime)
        data_object = {"Start":next_startDate.strftime("%Y-%m-%d"), "Finish":next_startDate.strftime("%Y-%m-%d"), "Day":day, "Start Time":a1.strftime("%H:%M:%S"), "End Time":endTime.strftime("%H:%M:%S")
        }
    else:
        return (startTime, endTime);
    return(startTime, endTime,data_object )
    

# import module
# import numpy
  
# # input year and month
# yearMonth = '2017-05'
  
# # getting date of first monday
# date = numpy.busday_offset(yearMonth, 0, 
#                            roll='forward', 
#                            weekmask='Mon')
  
# # display date
# print(date)


    
## function to automate calendar startDates and intervals
def automateCalendar(name, start_hour, start_minute ):
    data_list = []
    
    startDate = datetime(year=2022, month=8, day=12)
    # n = no. of startDates
    n=1
    print("n: ", n)
    #Calculates the startDate date and time
    #startDate = datetime(year=start_year, month=start_month, day=start_day, hour=start_hour, minute=start_minute, second=00)
    # if condition to check if correct name and correct corresponding date is entered
    yearMonth = startDate.strftime("%Y-%m")
    print("YEAR MONTH: ", yearMonth)
    #Find Monday
    if name == "9M21":
        startDate = numpy.busday_offset(yearMonth, 0, roll = 'forward', weekmask='Mon').astype(datetime)
    if name == "9M11":
        startDate = numpy.busday_offset(yearMonth, 0, roll = 'forward', weekmask='Mon').astype(datetime)+timedelta(days=+7)
    #Find Tuesday
    if name == "9U21":
        startDate = numpy.busday_offset(yearMonth, 0, roll = 'forward', weekmask='Tue').astype(datetime)
    if name == "9U11":
        startDate = numpy.busday_offset(yearMonth, 0, roll = 'forward', weekmask='Tue').astype(datetime)+timedelta(days=+7)
    #Find Wednesday
    if name == "9W21":
        startDate = numpy.busday_offset(yearMonth, 0, roll = 'forward', weekmask='Wed').astype(datetime)
    if name == "9W11":
        startDate = numpy.busday_offset(yearMonth, 0, roll = 'forward', weekmask='Wed').astype(datetime)+timedelta(days=+7)
    #Find Thursay
    if name == "9H21":
        startDate = numpy.busday_offset(yearMonth, 0, roll = 'forward', weekmask='Thu').astype(datetime)
    if name == "9H11":
        startDate = numpy.busday_offset(yearMonth, 0, roll = 'forward', weekmask='Thu').astype(datetime)+timedelta(days=+7)
    #Find Friday
    if name == "9F21":
        startDate = numpy.busday_offset(yearMonth, 0, roll = 'forward', weekmask='Fri').astype(datetime)
    if name == "9F11":
        startDate = numpy.busday_offset(yearMonth, 0, roll = 'forward', weekmask='Fri').astype(datetime)+timedelta(days=+7)
        
    print("New date: ", startDate)
 
    start_datetime = datetime(year=startDate.year,month=startDate.month, day=startDate.day, hour=start_hour, minute=start_minute, second=00 )
    
    

    #print("startDate: ", startDate.strftime("%Y-%m-%d"))
    day = startDate.strftime("%A")
    print("day: ", day)
    #tom -> calculates dates for alternating work days, like every other Friday
    tom = timedelta(days=+14)
    #function to calculate startDate intervals
    if name=="9F11" or name == "9F21":
        startTime, endTime = automate_time(start_hour, start_minute,  start_datetime, name)
        data_object = {"Start":startDate.strftime("%Y-%m-%d"), "Finish":startDate.strftime("%Y-%m-%d"), "Day":day, "Start Time":startTime.strftime("%H:%M:%S"), "End Time" :endTime.strftime("%H:%M:%S")
        }
        data_list.append(data_object)
    else: # for all other calendars
        startTime, endTime , data_object_returned= automate_time(start_hour, start_minute, start_datetime, name)
        
        data_object = {"Start":startDate.strftime("%Y-%m-%d"), "Finish":startDate.strftime("%Y-%m-%d"), "Day":day, "Start Time":startTime.strftime("%H:%M:%S"), "End Time" :endTime.strftime("%H:%M:%S")
        }
        data_list.append(data_object)
        data_list.append(data_object_returned)
        
        
    n+=1

    while n<=3:
        
        print()
        print("n: ", n)
        new_startDate = startDate+tom   #calculates the next alternating startDates
        startDate = datetime(year=new_startDate.year, month=new_startDate.month, day=new_startDate.day, hour=start_hour, minute=start_minute, second=00)
        print("startDate: ", startDate.strftime("%Y-%m-%d"))
        print("day: ", new_startDate.strftime("%A"))
        if name=="9F11" or name == "9F21":
            startTime, endTime = automate_time(start_hour, start_minute,  startDate, name)
            data_object = {"Start":startDate.strftime("%Y-%m-%d"), "Finish":startDate.strftime("%Y-%m-%d"), "Day":day, "Start Time":startTime.strftime("%H:%M:%S"), "End Time" :endTime.strftime("%H:%M:%S")
            }
            data_list.append(data_object)
        else: # for all other calendars
            startTime, endTime , data_object_returned= automate_time(start_hour, start_minute,  startDate, name)
            
            data_object = {"Start":startDate.strftime("%Y-%m-%d"), "Finish":startDate.strftime("%Y-%m-%d"), "Day":day, "Start Time":startTime.strftime("%H:%M:%S"), "End Time" :endTime.strftime("%H:%M:%S")
            }
            data_list.append(data_object)
            data_list.append(data_object_returned)

        n+=1
        
        
    print()
    print("done function")
    return (data_list)

        #return  ("Start date: ",startDate.strftime("%Y-%m-%d"))
        #return [startDate.strftime("%Y-%m-%d"),endDate.strftime("%Y-%m-%d"), new_startDate.strftime("%A"), startTime, endTime, n-1]
    

### TESTING #####
    ## MUST ENTER Year FROM AS A 4-IGIT, 2022
    ## MUST ENTER MONTHS FROM 1-9 AS A SINGLE DIGIT, 4 not 04
    ## MUST ENTER DAYS FROM 1-9 AS A SINGLE DIGIT, 9 not 09
    ## MUST ENTER HOUR FROM 1-9 AS A SINGLE DIGIT, 4 not 04
    ## MUST ENTER MINUTE FROM 1-9 AS A SINGLE DIGIT, 4 not 04

    ##Python function , def automateCalendar(name, start_year, start_month, start_day, start_hour, start_minute ), 
        # e.g automateCalendar("9F11", 2022, 8, 5, 6, 30)
    # Arguments ( Only name is passed as String, all other arguments as integers)

    ## START FROM AUGUST 2022 

        # 9M11 - Monday: 2022-8-8  - DONE
        # 9U11 - Tuesday 2022-8-9
        # 9W11 - Wednesday 2022-8-10
        # 9H11 - Thursday 2022-8-11
        # 9F11 - Friday: 2022-8-12

        # 9M21 - Monday: 2022-8-1
        # 9U11 - Tuesday 2022-8-2
        # 9W11 - Wednesday 2022-8-3
        # 9H11 - Thursday 2022-8-4
        # 9F11 - Friday: 2022-8-5
    
    ## DATA TO ENTER FOR TESTING
        ## Calendar Name and startDate date MUST match, otherwise does not output any startDates
            ##Correct: name "9M11" - First Monday off -> correct date: 2022-08-08, Monday (would work for 2022-08-01 also because that is Monday)
            ##Incorrect: name "9M11" - First Monday off -> incorrect date: 2022-08-02, Tuesday 
        ## Enter the time startDate starts

# print(len(result))

# for o in result:
#     print(o)
 #### SENDING TO CLICK ####
 ## IMPORTS ## 
# def post_body_forClick(someArrayArg, someCalendarID):
# # TODO: Create the final Post Body function to leverage the ClickSoftware API to update Calendars like what you did in PostMan
#     postBody = {}
    
#     return postBody
    
# def post_body_forClick(calendarObj):
# # # TODO: Create the final Post Body function to leverage the ClickSoftware API to update Calendars like what you did in PostMan
#     postBody = calendarObj
        
    
#     return postBody


def create_weeklyInterval(start, finish, day, startTime, endTime):
# TODO: Add arguments to this function
    weeklyInterval = {
        "OverwriteExisting": True,
        "Start": start,
        "Finish": finish,
        "Status": "Work",
        "WeeklyIntervalStart": {
            "Day": day,
            "Time": startTime
        },
        "WeeklyIntervalFinish": {
            "Day": day,
            "Time": endTime
        },
    }
    return weeklyInterval

# Empty Array
timePhasedWeeklyLevelArray = []

# prodCheck = False
# env = 'DEV'
# params = ''
# clickObj = 'Calendar'

# def UpdateClickObject(data, URL, username, password):
# def GetClickObject(obj, PARAMS, url, username, password):

obj = GetClickObject(clickObj, params, prodObjectCheck(prodCheck), environmentUsr(env), environmentPwd(env) )
#obj = GetClickObject(clickObj, 'https://fse-na-sb-int01.cloud.clicksoftware.com/so/api/Services/Calendar/GetCalendarIntervals', prodObjectCheck(prodCheck), environmentUsr(env), environmentPwd(env) )
#print(obj)
print(len(obj))
count=0
obj_9 = []
for o in obj:
    x = o['Name'].split()  # name
    if x[0][0] == '9':
        # count+=1
        # print(count, x[0])
        obj_9.append(o)
print(len(obj_9))
print(obj_9)
print()
# num = 0

for o1 in obj_9:
    count+=1
    
    x1 = o1['Name'].split() #name
    print(count, x1[0])
    name = x1[0][0:4]
    calendarName = x1[0]
    print(calendarName)
    
    key = o1["Key"]
    print("Key:", key)
    
    y1 = o1['Name'].split(":") #start_time
    hour = y1[1][0]
    min = y1[1][1:3]
    print("NEW CALENDAR")
    result = automateCalendar(name, int(hour), int(min))
    print("Type result: ", type(result))
    # print("Result: ", len(result))

    ## Function to convert string to datetime
    # datetime.strptime(date_string, format)
    for o2 in result:
        print()
        print(o2)
        # string str = DateTime.Now.ToString("yyyy-MM-dd'T'HH:mm:ss.fffffff'Z'");
        start = o2["Start"]
        # print(start)
        print("TYPE Start: ", type(start))
        start2 = datetime.strptime(start, "%Y-%m-%d")
        # print(start2)
        start3 = datetime.strftime(start2, "%Y-%m-%dT%H:%M:%S")
        print("Start3: ", start3)
        # print(type(start3))
        finish_new = start2+timedelta(days=+7)
      
        finish = o2["Finish"]
        finish2= datetime.strptime(finish, "%Y-%m-%d")
        finish3 = datetime.strftime(finish_new, "%Y-%m-%dT%H:%M:%S")
        print("Finish 3: ", finish3)

        day = o2["Day"]
        startTime = o2["Start Time"]
        endTime = o2["End Time"]
        timePhasedWeeklyLevelArray.append(create_weeklyInterval(start3, finish3, day, startTime, endTime))
        # print("Time array:", len(timePhasedWeeklyLevelArray))  
        
        # calendarObj = {"@objectType": "Calendar", "CalendarKey": key, "Name": name, "CalendarIntervals" : {"TimePhasedWeeklyInterval": timePhasedWeeklyLevelArray}}
        
        calendarObj = {"CalendarKey": key, "Name": calendarName, "CalendarIntervals" : {"TimePhasedWeeklyInterval": timePhasedWeeklyLevelArray, "OverwriteExisting": True} }
    print()
    # body = post_body_forClick(calendarObj)
    # print(body)
    # print()

    print("CALENDAR DONE!!")
    print()

    print("Updating Click Objects")
    URL = "https://fse-na-sb-int01.cloud.clicksoftware.com/so/api/Services/Calendar/UpdateCalendarIntervals?$filter=(contains(Name,'9F21-UC3:630-400'))"
    UpdateClickObject(calendarObj,URL , environmentUsr(env), environmentPwd(env))
    # UpdateClickObject(calendarObj, prodObjectCheck(prodCheck), environmentUsr(env), environmentPwd(env))
    print()
    #print(calendarObj)
    # print(calendarObj["CalendarKey"])
    # print(calendarObj["Name"])
    # print(*calendarObj["CalendarIntervals"]["TimePhasedWeeklyInterval"], sep = "\n")
    result=[]
    timePhasedWeeklyLevelArray=[]
    # print("Result:",len(result))
    # print("Time array:", len(timePhasedWeeklyLevelArray))
    # num+=1 
    # if num == 2: 
    #  break
    break



print("DONE !!")
