# This code sample uses the 'requests' library:
# http://docs.python-requests.org

import datetime as dt

import DefaultConfig as config
import JiraSearch as search
import Functions as func
import ExcelWorkbooks as excel
import sys

if len(sys.argv) == 2 and sys.argv[1] == 'A':
    reportList = config.components
else:
    reportList = func.getReportListFromInput()

start = dt.datetime.now(dt.timezone.utc)
print("Start at: " + str(start))

func.fillFixHolidays()
func.fillVariableHolidays()
func.fillTotalMonthHours()

# func.populateSquads()

# process reports
for component in reportList:
    totalIssues = search.byJQL(component)
    func.createCSVByResponseList(component)

func.calculateRemainingHours()

#excel.refreshAllWorkbooksData()

end = dt.datetime.now(dt.timezone.utc)
print("End at: " + str(end))
dif = end - start
dif = func.getTime(dif)
print("Time: " + str(dif))
