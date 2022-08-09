def post_body_forClick(someArrayArg, someCalendarID):
# TODO: Create the final Post Body function to leverage the ClickSoftware API to update Calendars like what you did in PostMan
    postBody = {}
    
    return postBody
    

def create_weeklyInterval(someArg, moreArgs, anotherArg):
# TODO: Add arguments to this function
    weeklyInterval = {
        "OverwriteExisting": True,
        "Start": "someDate",
        "Finish": "someOtherDate",
        "Status": "Work",
        "WeeklyIntervalStart": {
            "Day": "SomeEnumDayOfWeek",
            "Time": "someTime"
        },
        "WeeklyIntervalFinish": {
            "Day": "SomeEnumDayOfWeek",
            "Time": "someTime"
        },
    }
    return weeklyInterval

# Empty Array
timePhasedWeeklyLevelArray = []

# Append one weekly Interval to array
timePhasedWeeklyLevelArray.append(create_weeklyInterval("someArg", 'moreArgs', 'anotherArg'))
