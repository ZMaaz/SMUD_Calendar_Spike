"""
.Title
Automating Click Calendars

.Description
The purpose of this library is to automate the need for end users to manually
input calendars for the next three years for multiple shifts such as: 9F11, 9F21, 9M11 et cetera.

.History
Original Release - MZubair - 7/28/2022
Code Review - SON - 08/31/2022
"""
import time
from datetime import date, timedelta, time, datetime
from AllThingsClickCopy import GetCalendarIntervals, GetClickObject, UpdateClickObject
from AllThingsClickCopy import prodObjectCheck
from AllThingsClickCopy import environmentUsr
from AllThingsClickCopy import environmentPwd
import json


prodCheck = False
env = 'DEV'
params = ''
clickObj = 'Calendar'
cal_dict = {"9M11": [4, 2, "Monday"], "9M21": [4, 9, "Monday"],
            "9U11": [3, 3, "Tuesday"], "9U21": [3, 10, "Tuesday"],
            "9W11": [2, 4, "Wednesday"], "9W21": [2, 11, "Wednesday"],
            "9H11": [1, 5, "Thursday"], "9H21": [1, 12, "Thursday"],
            "9F11": [0, 6, "Friday"], "9F21": [0, 13, "Friday"]}



def automate_time(startDate, name):
    """ When startDate is provided, this function provides us with
        corresponding friday's of the same week.
        Note. if condition to schedule short-Friday-startDates for
        alternating Mon,Tues,Wed,Thurs. It excludes calendars 9F11 and 9F21.
    """
    if name in cal_dict:
        next_day = timedelta(days = +0)

        #if conditions to make sure that calendar name and dates match
        next_day = timedelta(days = +cal_dict[name][0])

        # next day symbolizes the alternate short shift usually fridays for the 9 hour work shifts
        next_startDate = startDate + next_day
        day = next_startDate.strftime("%A")

        return {
            "Start":next_startDate.strftime("%Y-%m-%d"),
            "Finish":next_startDate.strftime("%Y-%m-%d"),
             "Day":day
        }

    return "Correct Cal_type not specified"


def automateCalendar(name, numOfshifts):
    """ Main function to create the shifts with dates and times"""
    data_list = []

    # Arbitrary date used to recognize shift patterns for 8/20/2022 - 8/20/2025
    startDate = datetime(year=2022, month=8, day=20)
    num_shifts = 1

    # The start date provides the next start of the interval
    startDate += timedelta(days= +cal_dict[name][1])
    # formatting into date time object
    start_datetime = datetime(
        year=startDate.year, month=startDate.month, day=startDate.day
        )

    day = startDate.strftime("%A") # pinned
    #tomorrow -> calculates dates for alternating work days, like every other Friday
    tomorrow = timedelta(days= +14)

    data_object = {
        "Start":startDate.strftime("%Y-%m-%d"),
        "Finish":startDate.strftime("%Y-%m-%d"),
        "Day":day
        }
    data_list.append(data_object)

    if (name != "9F11" and name != "9F21"):

        data_object_returned= automate_time(start_datetime, name)
        data_list.append(data_object_returned)

    num_shifts += 1
    while num_shifts <= numOfshifts:
        #calculates the next alternating startDates
        new_startDate = startDate + tomorrow
        startDate = datetime(
            year=new_startDate.year,
            month=new_startDate.month,
            day=new_startDate.day
            )

        data_object = {
            "Start":startDate.strftime("%Y-%m-%d"),
            "Finish":startDate.strftime("%Y-%m-%d"),
            "Day":day
            }

        data_list.append(data_object)

        if (name!="9F11" and name != "9F21"):
            data_object_returned= automate_time(startDate, name)
            data_list.append(data_object_returned)

        num_shifts += 1

    #print("done function")
    return (data_list)


# Functions for creating Intervals for each status:
# OptionalWork, Work, Appointment, Routine
def create_weeklyInterval(startDate, endDate, workStatus):
    weeklyIntervalOptional = {
        "OverwriteExisting": True,
        "TimeInterval":{
            "Start": startDate,
            "Finish": endDate
        },
        "Status": workStatus,
        }
    return weeklyIntervalOptional

def create_weeklyIntervalAppnt(startDate, endDate):
    weeklyIntervalAppnt = {
        "OverwriteExisting": True,
        "TimeInterval": {
          "Start": startDate,
          "Finish": endDate
        },
        "Shift": 1436377088
        }
    return weeklyIntervalAppnt

def create_weeklyIntervalRoutine(startDate, endDate):
    weeklyIntervalRoutine = {
    "OverwriteExisting": True,
    "TimeInterval": {
        "Start": startDate,
        "Finish": endDate
    },
    "Shift": 1436368896
    }
    return weeklyIntervalRoutine

################# MAIN #################
# Empty Array
yearlyLevelArray = []
YearlyShiftLevelArray = []

obj = GetClickObject(clickObj, params, prodObjectCheck(prodCheck), environmentUsr(env), environmentPwd(env) )

obj_9 = []
## Creating a list of Calendars with names starting with "9"
for o in obj:
    x = o['Name'].split()  # name
    if x[0][0] == '9':
        obj_9.append(o)

name_num = 1

for o1 in obj_9:
    print()
    print("NEW CALENDAR")
    x1 = o1['Name'].split() #name
    name_num += 1
    name = x1[0][0:4]
    calendarName = x1[0]
    print(calendarName)

    key = o1["Key"]
    print("Key:", key)


  ## Url for getting Calendar Intervals
    URL_get = "https://fse-na-sb-int01.cloud.clicksoftware.com/so/api/Services/Calendar/GetCalendarIntervals"
    Prod_URL_get = "https://fse-na-int01.cloud.clicksoftware.com/so/api/Services/Calendar/GetCalendarIntervals"

    ### Get Intervals of Optional
    data_optional = {
    "Calendar": key,
    "IncludeBase": True,
    "RequestedYearlyLevel": {
        "UseCalendarTimeZone": True,
        "TimeInterval": {
            "Start": "08/29/2022",
            "Finish": "09/02/2022"
        },
        "Status": "OptionalWork"
    },
    "RequestedWeeklyLevel": {
        "Status": "OptionalWork"
    },
    "RequestedTimePhasedWeeklyLevel": {
        "TimeInterval": {
            "Start": "08/29/2022",
            "Finish": "09/02/2022"
        },
        "Status": "OptionalWork"
    }
    }

    ### Get Intervals of Work
    data_work = {
    "Calendar": key,
    "IncludeBase": True,
    "RequestedYearlyLevel": {
        "UseCalendarTimeZone": True,
        "TimeInterval": {
            "Start": "08/28/2022",
            "Finish": "09/02/2022"
        },
        "Status": "Work"
    },
    "RequestedWeeklyLevel": {
        "Status": "Work"
    },
    "RequestedTimePhasedWeeklyLevel": {
        "TimeInterval": {
            "Start": "08/28/2022",
            "Finish": "09/02/2022"
        },
        "Status": "Work"
    }
    }

    ### Get Intervals of Crews Appointment
    data_at = {

    "Calendar": key,
    "IncludeBase": True,
      "RequestedWeeklyShiftLevel": {
        "Shift": {
              "@objectType": "Group",
              "Key": 1436377088,
              "Revision": 1,
              "Name": "SMUD - Svc Crews Appointment"
            }
    }
    }

    ### Get Intervals of Crews Routine
    data_rt = {

    "Calendar": key,
    "IncludeBase": True,
      "RequestedWeeklyShiftLevel": {
        "Shift": {
              "@objectType": "Group",
              "Key": 1436368896,
              "Revision": 2,
              "Name": "SMUD - Svc Crews Routine"
            }
    }
    }


    # Work response
    res1 = GetCalendarIntervals(data_optional,URL_get , environmentUsr(env), environmentPwd(env))
    resJson1 = json.loads(res1)
    if len(resJson1['WeeklyLevel']) > 0:
        start_optional = resJson1['WeeklyLevel'][1]['WeeklyIntervalStart']['Time']
        end_optional = resJson1['WeeklyLevel'][1]['WeeklyIntervalFinish']['Time']

    #Optional Response
    res2 = GetCalendarIntervals(data_work,URL_get , environmentUsr(env), environmentPwd(env))
    resJson2 = json.loads(res2)
    start_work = resJson2['WeeklyLevel'][1]['WeeklyIntervalStart']['Time']
    end_work = resJson2['WeeklyLevel'][1]['WeeklyIntervalFinish']['Time']

    result = automateCalendar(name)
    # Keeps count of number of shifts in Result list
    count = 0
    while count<len(result):
        startDate = result[count]['Start']  ## 2022-08-20
        start2 = datetime.strptime(startDate, "%Y-%m-%d")
        if (len(resJson1['WeeklyLevel'])) > 0:
            ## 2nd optional Shift
            startOptional_time = datetime.strptime(start_optional, "%H:%M:%S").time()
            date1_optional = datetime(start2.year, start2.month, start2.day, startOptional_time.hour, startOptional_time.minute, startOptional_time.second)
            weeklyStartDate_optional = datetime.strftime(date1_optional, "%Y-%m-%dT%H:%M:%S")

            endOptional_time = datetime.strptime(end_optional, "%H:%M:%S").time()
            date2_optional = datetime(start2.year, start2.month, start2.day, endOptional_time.hour, endOptional_time.minute, endOptional_time.second)
            weeklyEndDate_optional = datetime.strftime(date2_optional, "%Y-%m-%dT%H:%M:%S")

            yearlyLevelArray.append(create_weeklyInterval(weeklyStartDate_optional, weeklyEndDate_optional, "OptionalWork"))

            if (start_optional != resJson1['WeeklyLevel'][2]['WeeklyIntervalStart']['Time']):
                # 3rd Optional Shift
                start_optional_2 = resJson1['WeeklyLevel'][2]['WeeklyIntervalStart']['Time']
                startOptional_time_2 = datetime.strptime(start_optional_2, "%H:%M:%S").time()

                end_optional_2= resJson1['WeeklyLevel'][2]['WeeklyIntervalFinish']['Time']
                endOptional_time_2 = datetime.strptime(end_optional_2, "%H:%M:%S").time()

                if (calendarName == "9F21-LA:630-1600"):
                    date1_optional_2 = datetime(start2.year, start2.month, start2.day, startOptional_time_2.hour-1, startOptional_time_2.minute, startOptional_time_2.second)
                    weeklyStartDate_optional_2 = datetime.strftime(date1_optional_2, "%Y-%m-%dT%H:%M:%S")


                    date2_optional_2 = datetime(start2.year, start2.month, start2.day, endOptional_time_2.hour-1, endOptional_time_2.minute, endOptional_time_2.second)
                    weeklyEndDate_optional_2 = datetime.strftime(date2_optional_2, "%Y-%m-%dT%H:%M:%S")

                    yearlyLevelArray.append(create_weeklyInterval(weeklyStartDate_optional_2, weeklyEndDate_optional_2, "OptionalWork"))
                else:
                    date1_optional_2 = datetime(start2.year, start2.month, start2.day, startOptional_time_2.hour, startOptional_time_2.minute, startOptional_time_2.second)
                    weeklyStartDate_optional_2 = datetime.strftime(date1_optional_2, "%Y-%m-%dT%H:%M:%S")


                    date2_optional_2 = datetime(start2.year, start2.month, start2.day, endOptional_time_2.hour, endOptional_time_2.minute, endOptional_time_2.second)
                    weeklyEndDate_optional_2 = datetime.strftime(date2_optional_2, "%Y-%m-%dT%H:%M:%S")

                    yearlyLevelArray.append(create_weeklyInterval(weeklyStartDate_optional_2, weeklyEndDate_optional_2, "OptionalWork"))


                if( calendarName == "9F21-LA:630-1600"):
                    # 1st Optional Shift
                    start_optional_3 = resJson1['WeeklyLevel'][3]['WeeklyIntervalStart']['Time']
                    startOptional_time_3 = datetime.strptime(start_optional_3, "%H:%M:%S").time()
                    date1_optional_3 = datetime(start2.year, start2.month, start2.day, startOptional_time_3.hour, startOptional_time_3.minute, startOptional_time_3.second)
                    weeklyStartDate_optional_3 = datetime.strftime(date1_optional_3, "%Y-%m-%dT%H:%M:%S")

                    end_optional_3= resJson1['WeeklyLevel'][3]['WeeklyIntervalFinish']['Time']
                    endOptional_time_3 = datetime.strptime(end_optional_3, "%H:%M:%S").time()
                    date2_optional_3 = datetime(start2.year, start2.month, start2.day, endOptional_time_3.hour, endOptional_time_3.minute, endOptional_time_3.second)
                    weeklyEndDate_optional_3 = datetime.strftime(date2_optional_3, "%Y-%m-%dT%H:%M:%S")

                    yearlyLevelArray.append(create_weeklyInterval(weeklyStartDate_optional_3, weeklyEndDate_optional_3, "OptionalWork"))
         #Work start time
        startWork_time = datetime.strptime(start_work, "%H:%M:%S").time()
        date1_work = datetime(start2.year, start2.month, start2.day, startWork_time.hour, startWork_time.minute, startWork_time.second)
        weeklyStartDate_work = datetime.strftime(date1_work, "%Y-%m-%dT%H:%M:%S")
        # 8 hour shift for Friday
        if (result[count]['Day'] == 'Friday'):
            endwork_time = datetime.strptime(end_work, "%H:%M:%S").time()
            date2_work = datetime(start2.year, start2.month, start2.day, endwork_time.hour-1, endwork_time.minute, endwork_time.second)
            weeklyEndDate_work = datetime.strftime(date2_work, "%Y-%m-%dT%H:%M:%S")
        else:  ## fi not Friday, keep it 9 hour
            endwork_time = datetime.strptime(end_work, "%H:%M:%S").time()
            date2_work = datetime(start2.year, start2.month, start2.day, endwork_time.hour, endwork_time.minute, endwork_time.second)
            weeklyEndDate_work = datetime.strftime(date2_work, "%Y-%m-%dT%H:%M:%S")

        yearlyLevelArray.append(create_weeklyInterval(weeklyStartDate_work, weeklyEndDate_work, "Work"))
        ## For more than 1 work shifts, e.g for 9F21-LA calendars
        if ((len(resJson2['WeeklyLevel'])) > 0):
            if (start_work != resJson2['WeeklyLevel'][2]['WeeklyIntervalStart']['Time']):
                start_time_1 = resJson2['WeeklyLevel'][2]['WeeklyIntervalStart']['Time']
                startWork_time_1 = datetime.strptime(start_time_1, "%H:%M:%S").time()
                date1_work_1 = datetime(start2.year, start2.month, start2.day, startWork_time_1.hour, startWork_time_1.minute, startWork_time_1.second)
                weeklyStartDate_work_1 = datetime.strftime(date1_work_1, "%Y-%m-%dT%H:%M:%S")

                end_time_1= resJson2['WeeklyLevel'][2]['WeeklyIntervalFinish']['Time']
                endWork_time_1 = datetime.strptime(end_time_1, "%H:%M:%S").time()
                date2_work_1 = datetime(start2.year, start2.month, start2.day, endWork_time_1.hour, endWork_time_1.minute, endWork_time_1.second)
                weeklyEndDate_work_1 = datetime.strftime(date2_work_1, "%Y-%m-%dT%H:%M:%S")

                yearlyLevelArray.append(create_weeklyInterval(weeklyStartDate_work_1, weeklyEndDate_work_1, "Work"))

            ## UC5 Calendars
            ## Appointment and Routine Shifts
            if (calendarName == '9F21-UC5:630-1600') or (calendarName == '9M21-UC5:630-1600'):
                print()
                #Appointment
                res3 = GetCalendarIntervals(data_at,URL_get , environmentUsr(env), environmentPwd(env))
                resJson3 = json.loads(res3)

                start_at_time = resJson3['WeeklyShiftInterval'][0]['WeeklyIntervalStart']['Time']
                start_at_time_1 = datetime.strptime(start_at_time, "%H:%M:%S").time()
                date1_at_1 = datetime(start2.year, start2.month, start2.day, start_at_time_1.hour, start_at_time_1.minute, start_at_time_1.second)
                weeklyStartDate_at_1 = datetime.strftime(date1_at_1, "%Y-%m-%dT%H:%M:%S")

                end_at_time= resJson3['WeeklyShiftInterval'][0]['WeeklyIntervalFinish']['Time']
                end_at_time_1 = datetime.strptime(end_at_time, "%H:%M:%S").time()
                date2_at_1 = datetime(start2.year, start2.month, start2.day, end_at_time_1.hour, end_at_time_1.minute, end_at_time_1.second)
                weeklyEndDate_at_1 = datetime.strftime(date2_at_1, "%Y-%m-%dT%H:%M:%S")

                YearlyShiftLevelArray.append(create_weeklyIntervalAppnt(weeklyStartDate_at_1, weeklyEndDate_at_1))
                ##Routine
                res4 = GetCalendarIntervals(data_rt,URL_get , environmentUsr(env), environmentPwd(env))
                resJson4 = json.loads(res4)

                start_rt_time = resJson4['WeeklyShiftInterval'][0]['WeeklyIntervalStart']['Time']
                start_rt_time_1 = datetime.strptime(start_rt_time, "%H:%M:%S").time()
                date1_rt_1 = datetime(start2.year, start2.month, start2.day, start_rt_time_1.hour, start_rt_time_1.minute, start_rt_time_1.second)
                weeklyStartDate_rt_1 = datetime.strftime(date1_rt_1, "%Y-%m-%dT%H:%M:%S")

                end_rt_time= resJson4['WeeklyShiftInterval'][0]['WeeklyIntervalFinish']['Time']
                end_rt_time_1 = datetime.strptime(end_rt_time, "%H:%M:%S").time()
                # 8 hour shift for Friday
                if (calendarName == '9F21-UC5:630-1600'):
                    date2_rt_1 = datetime(start2.year, start2.month, start2.day, end_rt_time_1.hour-1, end_rt_time_1.minute, end_rt_time_1.second)
                    weeklyEndDate_rt_1 = datetime.strftime(date2_rt_1, "%Y-%m-%dT%H:%M:%S")
                else:
                    #8 hour shift for Friday
                    if (result[count]['Day'] == 'Friday'):
                        date2_rt_1 = datetime(start2.year, start2.month, start2.day, end_rt_time_1.hour-1, end_rt_time_1.minute, end_rt_time_1.second)
                        weeklyEndDate_rt_1 = datetime.strftime(date2_rt_1, "%Y-%m-%dT%H:%M:%S")
                    else:
                        date2_rt_1 = datetime(start2.year, start2.month, start2.day, end_rt_time_1.hour, end_rt_time_1.minute, end_rt_time_1.second)
                        weeklyEndDate_rt_1 = datetime.strftime(date2_rt_1, "%Y-%m-%dT%H:%M:%S")

                YearlyShiftLevelArray.append(create_weeklyIntervalRoutine(weeklyStartDate_rt_1, weeklyEndDate_rt_1))

        count+=1


    calendarObj = {"CalendarKey": key, "Name": calendarName, "CalendarIntervals" : {"YearlyLevel": yearlyLevelArray,"YearlyShiftLevel": YearlyShiftLevelArray, "WeeklyLevel": [], "WeeklyShiftLevel": [], "TimePhasedWeeklyLevel": [] }, "OverwriteExisting": True }

    #print(calendarObj)

    print("Updating Click Objects")
    # #Update Calendar URL
    URL_update = "https://fse-na-sb-int01.cloud.clicksoftware.com/so/api/Services/Calendar/UpdateCalendarIntervals?$filter=(contains(Name,'9F21-UC3:630-400'))"
    UpdateClickObject(calendarObj,URL_update , environmentUsr(env), environmentPwd(env))
    print()
    print(*calendarObj["CalendarIntervals"]["YearlyLevel"], sep = "\n")
    print(*calendarObj["CalendarIntervals"]["YearlyShiftLevel"], sep = "\n")
    result=[]
    yearlyLevelArray=[]
    YearlyShiftLevelArray = []
    # num+=1
    # if num == 9:
    #  break
    # # break

print("DONE !!")
