'''
barrj4

Script will intake combat log and OBS stream log to determine location of all pulls during stream.

'''

import datetime
import os
import re

current_year = 2022  #WHAT YEAR IS IT

streamDate = '06142022' #modify to user input

wowLogLocation = 'D:\\World of Warcraft\\_retail_\\Logs'

obsLogLocation = 'C:\\Users\\Jeffrey\\AppData\\Roaming\\obs-studio\\logs'

outputLocation = 'C:\\Users\\Jeffrey\\Documents\\Python\\StreamMarkers' #should probably change this to automatically update based on location of the script.

def convertDate(inputDate):
    #Will need to change the date format from input to two types: WCL format and OBS format based on their file names.
    outputDate = []
    month = inputDate[:2]
    day = inputDate[2:4]
    year = inputDate[4:]

    wclDate = month + day + year[2:]
    obsDate = '%s-%s-%s' % (year,month,day)
    gDate = datetime.date(int(year),int(month),int(day))

    outputDate = [wclDate,obsDate,gDate]
    return outputDate

def importWCL(date):
    #import WCL and export the file as list of strings?
    logString = 'WoWCombatLog-' + date
    for file in os.listdir(wowLogLocation):
        if file.startswith(logString):
            filepath = os.path.join(wowLogLocation,file)
            f = open(filepath, 'r')
            content = f.readlines()
            f.close()
            return content
    print ('Warcraft Log file from this date not found')
    return 0
def importOBSL(date):
    #import OBS Logs and export the file as a list of strings
    logString = date
    for file in os.listdir(obsLogLocation):
        if file.startswith(logString):
            filepath = os.path.join(obsLogLocation,file)
            f = open(filepath, 'r')
            content = f.readlines()
            f.close()
            return content
    print ('OBS Log file from this date not found')
    return 0
def parseWCL(logText):
    #intake the log text variable and output tuple/dictionary relating pull number and time in local timezone
    #Should probably include some data on what encounter
    listPulls = []
    for line in logText:
        if 'ENCOUNTER_START' in line:
            temp_line = re.split('[ /:.]',line)
            for i in range(0, len(temp_line)):
                try:
                    temp_line[i] = int(temp_line[i])
                except:
                    continue
            temp_dt = datetime.datetime(current_year,temp_line[0],temp_line[1],temp_line[2],temp_line[3],temp_line[4])
            listPulls.append(temp_dt)

    return listPulls
def parseOBSL(logText,gDate):
    #intake the log text variable from OBS and output stream start date/time
    #should probably use strptime instead
    for line in logText:
        if 'Streaming Start' in line:
            temp_line = re.split('[ /:.]',line)
            for i in range(0, len(temp_line)):
                try:
                    temp_line[i] = int(temp_line[i])
                except:
                    continue
            streamDT = datetime.datetime(gDate.year,gDate.month,gDate.day,temp_line[0],temp_line[1],temp_line[2])
            return streamDT
    return 0
def convertStamps(timeStamps):
    #take pull time list and convert from actual time to stream time, export in new time stamps
    #not used
    return 0
def main():
    #convert date for inputs
    wclDate,obsDate,gDate = convertDate(streamDate)
    #import WCL
    wcl_txt = importWCL(wclDate)
    #import OBS Logs
    obs_txt = importOBSL(obsDate)
    #Get time stamps from the WCL text
    pullTimes = parseWCL(wcl_txt)
    #Get stream start time from OBS log text
    streamStart = parseOBSL(obs_txt,gDate)
    #Do math to convert pull timestamps to stream time stamps
    print('0:00 Stream Start')
    for i in range(0,len(pullTimes)):
        temp_mark = str(pullTimes[i] - streamStart)
        print(temp_mark + ' Pull ' + str(i+1))

main()

    
