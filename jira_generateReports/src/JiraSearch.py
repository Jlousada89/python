from jira.client import JIRA
from datetime import datetime, timedelta
import DefaultConfig as config
import DefaultConfig as default
import Functions as f


def byJQL(component):
    print("Searching " + component + " issues ... ")
    jql = config.jql.replace("component", component)

    print("Connecting to JIRA ... ")
    options_server = {'server': default.jiraURI}
    jira = JIRA(server=default.jiraURI, basic_auth=(default.jiraUser, default.jiraToken))

    print("Initializing ... ")
    cnt = 0
    existsMore = True
    got = 0
    default.workLogList.clear()
    default.totalByWeek.clear()
    default.totalByWeekJoseManuel.clear()

    while existsMore:
        start_idx = default.block_num * default.block_size
        issues = jira.search_issues(jql, got, default.block_size)

        got += len(issues)
        print(got)
        print(issues)

        if got < 50:
            existsMore = False

        if len(issues) == 0:
            f.clearAll()
            return cnt

        default.block_num += 1
        for issue in issues:

            # print(default.point,sep="",end="\n",flush=True)

            cnt += 1

            # if cnt == 50: return None

            issueFields = issue.fields
            # issueType = issueFields.issuetype.name
            # issueStatus = issueFields.status.name
            # firstResponseDate = issueFields.customfield_10000
            # assignee = issueFields.assignee
            # issueResolution = issueFields.resolution
            #
            # if  issueFields.resolution != None:
            #     issueResolution = issueResolution.name
            # else:
            #     issueResolution = default.emptyStr

            # issueInfo = str(issueType) + default.semicolon
            # issueInfo += str(issue.key) + default.semicolon
            # issueInfo += str(issueFields.summary) + default.semicolon
            # issueInfo += str(issueStatus) + default.semicolon
            # issueInfo += str(issueResolution) + default.semicolon
            # issueInfo += str(assignee) + default.semicolon
            # issueInfo += str(issueFields.created) + default.semicolon

            componentName = ""
            cfp = ""
            po = ""

            isRightComponent = False
            for issueComponent in issueFields.components:
                if str(issueComponent) == component:
                    isRightComponent = True
                    #print("isRightComponent true")
                    break

            if isRightComponent is False:
                #print("isRightComponent false")
                continue

            haveRequest = False
            for label in issueFields.labels:
                for financingLabel in default.labels:
                    if label == financingLabel:
                        haveRequest = True
                        componentName += label
                        #print("break here")
                        break

                if label[0:3] == "CFP":
                    cfp = label

                if label[0:2] == "PO":
                    po = label

            if haveRequest is False:
                continue

            # doesn't have the right attributes
            if componentName == "":
                continue

            worklogs = jira.worklogs(issue.key)

            # print(issue.key)
            for worklogId in worklogs:
                # print(worklogId)
                worklog = jira.worklog(issue.key, worklogId)
                dayExtended = worklog.started[0:10]
                # year = worklog.started[0:4]
                # month = worklog.started[5:7]
                # day = worklog.started[8:10]
                author = worklog.author
                timeSpentSeconds = worklog.timeSpentSeconds
                timeSpentMinutes = timeSpentSeconds / 60
                timeSpentHours = timeSpentMinutes / 60

                workLogComment = ""

                try:
                    if worklog.comment is not None:
                        workLogComment = worklog.comment

                except:
                    if componentName != default.componentNotCommented:
                        print("issue: " + issue.key + " doesn't have a comment in some worklog")
                        continue

                # week = datetime.date(int(year), int(month), int(day)).isocalendar()[1]
                #print(str(author) + "::" + str(workLogComment))
                #print(worklog.started)
                try:
                    datetimeObj = datetime.strptime(worklog.started, '%Y-%m-%dT%H:%M:%S.%f+0000')
                except:
                    datetimeObj = datetime.strptime(worklog.started, '%Y-%m-%dT%H:%M:%S.%f+0100')

                monday = datetimeObj - timedelta(days=datetimeObj.weekday())

                key = cfp + default.doublePoint + po + default.doublePoint + componentName + default.doublePoint + str(monday)[0:10]

                #print("key: " + key)
                #print("timeSpentHours: " + str(timeSpentHours))

                if key in default.totalByWeek:
                    default.totalByWeek[key] += timeSpentHours
                else:
                    default.totalByWeek[key] = timeSpentHours



                # default.totalByWeek[str(monday)[0:10]].append(timeSpentHours)
                timeSpentHoursStr = str(timeSpentHours).replace('.', ',')

                wlog = str(author) + default.semicolon
                wlog += str(monday)[0:10] + default.semicolon
                wlog += dayExtended + default.semicolon
                wlog += componentName + default.semicolon

                wlog += cfp + default.semicolon
                wlog += po + default.semicolon

                wlog += workLogComment + default.semicolon + timeSpentHoursStr

                #print(wlog)

                default.workLogList.append(wlog)

    print("Search End!")
