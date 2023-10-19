#xlwings needs a license 
#import xlwings as xw

import os
import DefaultConfig as conf


def refreshAllWorkbooksData():
    # app = xw.App()

    print("refreshAllWorkbooksData INI")

    dir = "jira/generateReports/output/" + str(conf.year) + "/"
    for file in os.listdir(dir):
        if file.endswith(".xlsx"):
            fileDir = os.path.join(dir, file)
            print(fileDir)
            #wb = xw.Book(fileDir)
            print("refresh data in workbook " + fileDir)
            wb.api.RefreshAll()


    print("refreshAllWorkbooksData END")