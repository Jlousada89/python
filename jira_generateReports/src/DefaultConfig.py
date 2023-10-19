# This Python file uses the following encoding: utf-8
from collections import defaultdict

import Config

# JIRA
jiraUser = Config.user
jiraURI = Config.endpoint
jiraToken = Config.token
JiraIssueLink = jiraURI + "/browse/"
jiraIssueWorkLog = jiraURI + "/rest/api/3/issue/{issueIdOrKey}/worklog"
components = ["component1","component2","component3"]
labels = ["label1", "label2", "label3"]
componentNotCommented = "label4" #tickets with label with no necessary comment 
jql = "<your_query>"

# Defaults
# utcTimeFormat = "%Y-%m-%dT%H:%M:%S.%f%z"
# dateFormat= "%Y-%m-%d"
semicolon = ";"
# doubleSemicolon = ";"
point = "."
doublePoint = ":"
# blankSpace = " "
# comma = ","
emptyStr = ""
# strOpenTime = "09:00"
# strCloseTime = "18:00"
# openTime = dt.timedelta(hours=9, minutes=0, seconds=0)
# closeTime = dt.timedelta(hours=18, minutes=0, seconds=0)
# workHours = 8
# workDays = 5
# OK="OK"
# KO="KO"
endLine = "\n"
# endLine2 = "\r"
# encoding = "utf-8"

resultsFile = "jira/generateReports/output/year/results.csv"
resultsFileHeader = "Nombre;Semana;Fecha;Iniciativa;CFP;PO;MYS;Horas;Total Semana"

# EMAIL parameteres
sender = Config.email_sender
password = Config.email_pwd

subject = "some subject text"
body = "some body text"
# smtp = "outlook.office365.com"
# smtp = "smtp.office365.com"
smtp = "52.98.159.18"
# port = 25
port = 587

# proxy settings
# proxy_host = ""
# proxy_port = 8080

# for Jira
block_size = 100
block_num = 0

# lists
workLogList = []

# Dictionary's
totalByWeek = defaultdict(list)
totalMonthHours = defaultdict(list)
totalMonthHoursByName = defaultdict(list)

receivers = ["<any email>"]

squadWD = []
squadBau = []
squadMas = []
teamMember = []
