
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
import datetime
import time
from datetime import timedelta, time, datetime


### FUNCTIONS ####

# Function to calculate shift intervals -> shift start and shift end times
def automate_time(start_hour, start_minute, shift, name):
    time_str = shift.strftime("%H::%M::%S")  # extracting time from the shift object into a string
    time_object = datetime.strptime(time_str, '%H::%M::%S') # converting time_str into datetime object
    
    a = time(start_hour, start_minute)  #shift start time
    
    #Calculating shift end time
    if (name == "9F11" or name == "9F21"):
        b = time_object+timedelta(days=+0, hours=+8, minutes=+30) 
    else:
        b = time_object+timedelta(days=+0, hours=+9, minutes=+30)

    print("Start Time: ",a )
    print("End Time: ",datetime.strptime(str(b), "%Y-%m-%d %H:%M:%S").time())
    
    #if condition to schedule short-Friday-shifts for alternating Mon,Tues,Wed,Thurs
    #It exlcudes calendars 9F11 and 9F21
    if (name == "9M11" or name == "9M21" or  name == "9U11" or name == "9U21" or name == "9W11" or name == "9W21" or name == "9H11" or name == "9H21"):
        #initializing next_day and next_shift variables
        next_day = timedelta(days=+0)
        next_shift = shift + next_day
        
        #if conditions to make sure that calendar name and dates match
        if ((name == "9M11" or name == "9M21") and (shift.strftime("%A")=="Monday")):
            next_day = timedelta(days=+4)
        elif ((name == "9U11" or name == "9U21") and (shift.strftime("%A")=="Tuesday")):
            next_day = timedelta(days=+3)
        elif ((name == "9W11" or name == "9W21")and (shift.strftime("%A")=="Wednesday")):
            next_day = timedelta(days=+2)
        elif ((name == "9H11" or name == "9H21") and (shift.strftime("%A")=="Thursday")):
             next_day = timedelta(days=+1)
        else:
            return ;
        
        next_shift = shift + next_day
        print("Next shift:", next_shift.strftime("%Y-%m-%d")) ## Friday
        print("Day: ", next_shift.strftime("%A"))    
        a1 = time(start_hour+1, start_minute, 00) ##new start time for Friday
        print("Start Time: ", a1)
        print("End Time: ",datetime.strptime(str(b),  "%Y-%m-%d %H:%M:%S").time())
    else:
        return;
    
## function to automate calendar shifts and intervals
def automateCalendar(name, start_year, start_month, start_day, start_hour, start_minute ):
    # n = no. of shifts
    n=1
    print("n: ", n)
    #Calculates the shift date and time
    shift = datetime(year=start_year, month=start_month, day=start_day, hour=start_hour, minute=start_minute, second=00)
    # if condition to check if correct name and correct corresponding date is entered
    if (((name == "9M11" or name == "9M21") and (shift.strftime("%A")=="Monday")) or ((name == "9U11" or name == "9U21") and (shift.strftime("%A")=="Tuesday")) or ((name == "9W11" or name == "9W21")and (shift.strftime("%A")=="Wednesday")) or ((name == "9H11" or name == "9H21") and (shift.strftime("%A")=="Thursday")) or ((name == "9F11" or name == "9F21") and (shift.strftime("%A")=="Friday"))):
        
        print("shift: ", shift.strftime("%Y-%m-%d"))
        print("day: ", shift.strftime("%A"))
        #tom -> calculates dates for alternating work days, like every other Friday
        tom = timedelta(days=+14)
        #function to calculate shift intervals
        automate_time(start_hour, start_minute,  shift, name)
        
        n+=1

        while n<=100:
            print()
            print("n: ", n)
            new_shift = shift+tom   #calculates the next alternating shifts
            shift = datetime(year=new_shift.year, month=new_shift.month, day=new_shift.day, hour=start_hour, minute=start_minute, second=00)
            print("Shift: ", shift.strftime("%Y-%m-%d"))
            print("day: ", new_shift.strftime("%A"))
            automate_time(start_hour, start_minute,  shift, name)
        
            n+=1
        print()
        print("done function")
        return ("Last Shift:", shift.strftime("%Y-%m-%d"))
    else: #if calendar name and corresponding date does not match
        print("Incorrect  calendar name, date or time")
        return;


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
        ## Calendar Name and shift date MUST match, otherwise does not output any shifts
            ##Correct: name "9M11" - First Monday off -> correct date: 2022-08-08, Monday (would work for 2022-08-01 also because that is Monday)
            ##Incorrect: name "9M11" - First Monday off -> incorrect date: 2022-08-02, Tuesday 
        ## Enter the time shift starts

print(automateCalendar("9M11", 2022, 8, 8, 6, 30))
print("DONE")


