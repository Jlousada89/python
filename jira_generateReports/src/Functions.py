import datetime as dt
import sys

import DefaultConfig as default
import WebHooks as wh
import Holidays as h
import Globals as globals
import DefaultConfig as config

def getHours(value):
    days, seconds = value.days, value.seconds
    hours = days * 24 + seconds // 3600
    return hours


def getMinutes(value):
    seconds = value.seconds
    minutes = (seconds % 3600) // 60
    return minutes


def getSeconds(value):
    seconds = value.seconds
    seconds = seconds % 60
    return seconds


def convertHoursToDays(hours):
    days = hours / 24
    intDays = int(days)
    hours = int((days - intDays) * 24)

    response = str(intDays) + "días " + str(hours)
    return response


def getTime(value):
    days, seconds = value.days, value.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    response = convertHoursToDays(hours) + default.doublePoint + str(minutes) + default.doublePoint + str(seconds)
    return response


def getTimeFromDatetime(value):
    days, seconds = value.day, value.second
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    response = convertHoursToDays(hours) + default.doublePoint + str(minutes) + default.doublePoint + str(seconds)
    return response


def getPercentage(value, total):
    return round((value / total) * 100, 2)


def clearAll():
    default.block_num = default.block_size = 0


def assignSquad(squad):
    switch = {
        'WDAPI': default.squadWD,
        'Support': default.squadBau,
        'mas': default.squadMas,
        'dev': default.teamMember
    }
    return switch.get(squad, [])


def getSquadConnector(squad):
    switch = {
        '1': wh.financingWebhook,
        '2': wh.managementWebHook
    }
    return switch.get(squad, [])


def fillFixHolidays():
    now = dt.datetime.now()
    h.holidays = {
        dt.date(now.year, 1, 1),
        dt.date(now.year, 4, 25),
        dt.date(now.year, 5, 1),
        dt.date(now.year, 6, 13),
        dt.date(now.year, 8, 15),
        dt.date(now.year, 10, 5),
        dt.date(now.year, 11, 1),
        dt.date(now.year, 12, 1),
        dt.date(now.year, 12, 8),
        dt.date(now.year, 12, 25)
    }  # you can add more here


def fillVariableHolidays():
    now = dt.datetime.now()
    for variableHoliday in h.variableHolidays:
        month = variableHoliday[0]
        day = variableHoliday[1]
        h.holidaysList.append(dt.date(now.year, month, day))


def fillTotalMonthHours():
    now = dt.datetime.now()

    for month in range(1, 12):
        default.totalMonthHours[month] = calculateTotalMonthHours(now.year, month)


def calculateTotalMonthHours(year, month):
    businessDays = 0
    for i in range(1, 32):
        try:
            thisDate = dt.date(year, month, i)
        except ValueError:
            break

        if thisDate.weekday() < 5 and thisDate not in h.holidaysList:  # Monday == 0, Sunday == 6
            businessDays += 1

    return businessDays


def createCSVByResponseList(component, sendemail=True):
    print("Creating CSV file(s)...")

    resultsFileName = default.resultsFile.replace("results", default.year + "_results_" + component)
    print("opening file1 " + resultsFileName + "... ")
    print("year: " + default.year)
    resultsFileName = resultsFileName.replace("year",default.year)
    print("opening file " + resultsFileName + "... ")
    resultsFile = open(resultsFileName, 'w')

    resultsFile.write(default.resultsFileHeader)
    resultsFile.write(default.endLine)

    for workLog in default.workLogList:
        workLogSeparated = workLog.split(";")
        name = workLogSeparated[1]
        _key = workLogSeparated[4] + default.doublePoint + workLogSeparated[5] + default.doublePoint + workLogSeparated[
            3] + default.doublePoint + workLogSeparated[1]
        hours = str(default.totalByWeek[_key] / 8).replace('.', ',')
        month = workLogSeparated[2][6:7]

        workLog += default.semicolon
        workLog += hours

        print(workLog)
        print("month: " + month + ":::Hours: " + hours)

        #if name not in default.totalMonthHoursByName:
        #    default.totalMonthHoursByName[name] = {month, hours}
        #    print("default.totalMonthHoursByName["+name+"] = " + default.totalMonthHoursByName[name] + "{month, hours}")
        #else:
        #    for value in default.totalMonthHoursByName[name]:
        #        print("value: " + value)
        #        _month = value[0]
        #       _hours = value[1] + hours
        #
        #         if _month == month:
        #             default.totalMonthHoursByName[name] = {month, _hours}

        resultsFile.write(workLog)
        resultsFile.write(default.endLine)

    resultsFile.close()

    if sendemail:
        print("send email not implemented yet")

    print("CSV file(s) created! ")


def calculateRemainingHours():
    for value in default.totalMonthHoursByName:
        print(value)

        name = value[0]
        monthHours = value[1]
        print(monthHours)

        for monthTotalHour in monthHours:
            month = monthTotalHour[0]
            hours = monthTotalHour[1]

            print(name + default.semicolon + month + default.semicolon + hours + default.semicolon + "Remaining: " + (
                        default.totalMonthHours[month] - hours))

def getReportListFromInput():
    control = True
    reportList = []
    while control:
        print("All reports list: ")
        print(config.components)
        if reportList:
            print("Your reports list: ")
            print(reportList)
        report = input("Select a report (All[" + globals.ALL + "], Generate[" + globals.GEN + "], Exit[" + globals.EXIT + "]):")
        if report == globals.EXIT:
            sys.exit()
        elif (report == globals.GEN or not report) and reportList:
            control = False
        elif report == globals.ALL or ((report == globals.GEN or not report) and not reportList):
            reportList = config.components
            control = False
        elif report not in config.components:
            print("Report not allowed")
        else:
            reportList.append(report)
    
    return reportList
