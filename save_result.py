# encoding =utf-8
from xlutils import copy
import os, time
import xlrd



def save_result(caseFile, stepResult, caseResult, resultPath):
    # 每步测试结果反写入excel
    data = xlrd.open_workbook(caseFile)
    newbook = copy.copy(data)
    # 将结果以String类型反写入用例step的第7列
    stepsheet = newbook.get_sheet(1)
    for i in stepResult.keys():
        stepsheet.write(int(i), 6, u'{}'.format(stepResult[i]))

    # 将结果以String类型反写入用例集的第3列
    casesheetR = data.sheet_by_index(0)
    casesheet = newbook.get_sheet(0)
    # 遍历用例集
    for j in range(1, casesheetR.nrows):
        caseNo = casesheetR.row_values(j)[0]
        caseSwitch = casesheetR.row_values(j)[1]
        for i in caseResult.keys():
            if str.lower(caseSwitch) == 'y' and str(caseNo) == i:
                casesheet.write(int(j), 2, u'{}'.format(caseResult[i]))
    if not os.path.exists(resultPath):
        os.makedirs(resultPath)
    reportFile = os.path.abspath(os.path.join(resultPath, 'Report@%s.xls' % time.strftime('%Y%m%d@%H%M%S')))
    newbook.save(reportFile)
    return reportFile
